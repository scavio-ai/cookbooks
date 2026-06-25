"""
LocalDealScout: find the best Walmart deals in a category.

A free alternative to deal-aggregator apps. Give it a product category. It
searches Walmart, ranks results by discount and value (price vs rating vs
review volume), and returns a clean buy list -- the standout deals worth
grabbing, with why each made the cut.

Built with LangChain create_agent, OpenAI tool calling, and langchain-scavio
Walmart tools.

Prerequisites:
  pip install langchain langchain-openai "langchain-scavio>=2.9" python-dotenv
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/local-deal-scout.py "robot vacuum under 200"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioWalmartProduct, ScavioWalmartSearch

load_dotenv(override=True)


SYSTEM_PROMPT = """You are LocalDealScout, a deal-ranking agent for Walmart.

## Workflow

1. Parse the request into a search query and any price ceiling.
2. Call ScavioWalmartSearch. If a price ceiling is implied, search with it in
   mind and ignore items above it.
3. From the results, rank deals using price, rating, and rating_count. Favor
   items that are well-rated (4.0+), have real review volume, and are clearly
   priced below typical for the category.
4. For the single best pick, call ScavioWalmartProduct for fuller detail to
   confirm it is in stock and genuinely a deal.
5. ANSWER:

   ## Top deals: <category>
   #N  <title>
   Price: <price>   Rating: <rating> (<rating_count> reviews)
   Why: <one line on why it is a deal>

   End with a single "Best overall" callout and a one-line reason.

## Rules
- Use only products returned by the tools. Never invent prices or ratings.
- Skip out-of-stock or unrated items unless nothing better exists.
- Keep the answer under 350 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [ScavioWalmartSearch(max_results=15), ScavioWalmartProduct()]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(request: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    request = " ".join(sys.argv[1:]) or "robot vacuum under 200"
    print(f"\nRequest: {request}\n{'-' * 60}")
    print(run(request))
