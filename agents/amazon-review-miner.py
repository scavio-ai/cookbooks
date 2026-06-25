"""
AmazonReviewMiner: mine an Amazon product's reviews for real signal.

Give it a product name. It finds the top ASIN, pulls full product detail
(rating distribution, review highlights, Q&A, specs), and extracts the
recurring praise and -- more usefully -- the recurring complaints and failure
modes buyers report. The research step before you buy or before you build a
competitor.

Built with LangChain create_agent, OpenAI tool calling, and langchain-scavio
Amazon tools.

Prerequisites:
  pip install langchain langchain-openai "langchain-scavio>=2.9" python-dotenv
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/amazon-review-miner.py "anker 737 power bank"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioAmazonProduct, ScavioAmazonSearch

load_dotenv(override=True)


SYSTEM_PROMPT = """You are AmazonReviewMiner. Given a product name, surface what
buyers actually say.

## Workflow

1. Call ScavioAmazonSearch for the product. Choose the best-matching organic
   (non-sponsored) result and note its ASIN.
2. Call ScavioAmazonProduct on that ASIN. Read every review-related field the
   response provides: overall rating, rating breakdown, review highlights,
   answered questions, and any "what customers say" summary.
3. ANSWER:

   ## <title>
   ASIN <asin>  --  <rating> stars across <reviews_count> reviews

   ### What buyers love
   - 3-5 bullets, each grounded in the data.

   ### What buyers complain about
   - 3-5 bullets. Prioritize durability/defect/fit/support issues.

   ### Verdict
   One paragraph: who it is right for and the single biggest risk.

## Rules
- Use only the returned data. Never fabricate quotes, ratings, or counts.
- If review detail is thin, say so rather than padding.
- Keep the answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [ScavioAmazonSearch(max_results=8), ScavioAmazonProduct()]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(product: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": product}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    product = " ".join(sys.argv[1:]) or "anker 737 power bank"
    print(f"\nProduct: {product}\n{'-' * 60}")
    print(run(product))
