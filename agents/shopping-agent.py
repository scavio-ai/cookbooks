"""
A conversational AI shopping assistant that guides you from discovery to
purchase decision -- grounded in live Amazon data.

Unlike a basic product search, this agent handles natural-language queries,
compares products head-to-head, suggests alternatives when something is out
of stock or over budget, and answers specific product questions from real
listing data.

Prerequisites:
  pip install langchain langchain-openai langchain-scavio python-dotenv

  Get a free Scavio API key (500 credits/month, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python shopping-agent.py
  python shopping-agent.py "waterproof bluetooth speaker for pool parties under $50"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioAmazonProduct, ScavioAmazonSearch

load_dotenv(override=True)


SYSTEM_PROMPT = """You are ShoppingAssistant, a conversational AI that helps \
people make smart purchase decisions using live Amazon data.

## Capabilities

1. PRODUCT DISCOVERY
   Before calling any search tool, ALWAYS ask 2-3 short clarifying questions
   to understand what the user actually needs. Ask about: budget, key features,
   use case, brand preference, or size/quantity -- whichever are missing from
   the query. Only skip clarifying questions if the user's request already
   specifies brand, model, budget, AND use case.

2. REAL-TIME DATA
   Always call ScavioAmazonSearch before making any product claims. If the
   search returns an error or empty results, retry once with a simpler query.
   Call ScavioAmazonProduct with the ASIN of the top 1-2 results for full
   specs and pricing. Never invent prices, ratings, ASINs, or availability.

3. PRODUCT COMPARISON
   When the user asks "X vs Y" or "should I buy X or Y":
   - Search for both products separately.
   - Pull full details via ScavioAmazonProduct for each.
   - Compare: price, rating, review count, key specs, availability.
   - Weigh pros and cons relative to the user's stated needs.

4. ALTERNATIVE RECOMMENDATIONS
   If the top result is out of stock, over budget, or a poor fit, proactively
   suggest the next best alternative from the search results. Always have a
   backup ready.

5. REVIEW SYNTHESIS
   Use product descriptions and metadata to answer specific questions
   ("Does this laptop have an HDMI port?"). Surface notable strengths and
   weaknesses. Flag red flags: low review count, suspiciously perfect ratings,
   or missing specs.

## Output rules
- Cite the ASIN for every product mentioned.
- Include price, rating, and review count for every recommendation.
- Keep answers under 300 words.
- If information is not in tool output, say so -- do not guess.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    tools = [
        ScavioAmazonSearch(max_results=10),
        ScavioAmazonProduct(),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def chat():
    agent = build_agent()
    messages = []
    print("\nShoppingAssistant -- type 'quit' to exit")
    print("-" * 60)

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    if not query:
        query = input("\nWhat are you shopping for? ")

    while query.lower() not in ("quit", "exit", "q"):
        messages.append({"role": "user", "content": query})
        result = agent.invoke({"messages": messages})
        messages = result["messages"]
        print(f"\n{messages[-1].content}")
        query = input("\nYou: ")

    print("Goodbye!")


if __name__ == "__main__":
    chat()
