"""
A minimal LangChain agent that researches Amazon products.

Give it a product query in natural language. It decides when to search
Amazon, when to pull full product details by ASIN, and returns a buy
recommendation grounded in real listings.

Prerequisites:
  pip install langchain langchain-openai langchain-scavio python-dotenv

  Get a free Scavio API key (500 credits/month, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python amazon-agent.py "best wired earbuds under $50"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioAmazonProduct, ScavioAmazonSearch

load_dotenv(override=True)


SYSTEM_PROMPT = """You are AmazonScout, a product research agent.

Workflow:
1. Call ScavioAmazonSearch to find 5 candidate products for the user's query.
2. Pick the 2 most promising ASINs (balance rating, review count, price).
3. Call ScavioAmazonProduct on each ASIN for full details.
4. Return a short recommendation: top pick, runner-up, one-line rationale
   each, and one red flag to watch for. Cite ASINs.

Rules:
- Never invent ASINs, prices, or ratings. Only use tool output.
- If a tool returns nothing useful, say so instead of guessing.
- Keep the final answer under 200 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [
        ScavioAmazonSearch(max_results=5),
        ScavioAmazonProduct(),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(query: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "best wired earbuds under $50"
    print(f"\nQuery: {query}\n{'-' * 60}")
    print(run(query))
