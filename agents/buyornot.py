"""
BuyOrNot: multi-platform product research that tells you whether to buy.

Ask it about any product and it fans out to Google, Amazon, Walmart,
YouTube, and Reddit. It synthesizes a verdict with pros, cons, the best
price across platforms, and red flags from real user reviews.

Prerequisites:
  pip install langchain langchain-openai langchain-scavio python-dotenv

  Get a free Scavio API key (500 credits/month, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/buyornot.py "Sony WH-1000XM5"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import (
    ScavioAmazonProduct,
    ScavioAmazonSearch,
    ScavioRedditPost,
    ScavioRedditSearch,
    ScavioSearch,
    ScavioWalmartProduct,
    ScavioWalmartSearch,
    ScavioYouTubeMetadata,
    ScavioYouTubeSearch,
)

load_dotenv(override=True)


SYSTEM_PROMPT = """You are BuyOrNot, a multi-platform product research \
analyst. Given a product, you investigate it across every available source \
and deliver a definitive buy-or-skip verdict.

## Parse the query

Extract the product name, brand, and model from the user's input. If the
query is vague (e.g., "a good blender"), pick the most popular product in
that category to evaluate.

## Workflow

IMPORTANT: Call only ONE tool per step. The API rate-limits concurrent
requests. Never call two search tools in the same turn.

1. AMAZON
   Call ScavioAmazonSearch for the product. Then call ScavioAmazonProduct
   on the top match to get full pricing, ratings, and specs.

2. WALMART
   Call ScavioWalmartSearch for the product. Then call ScavioWalmartProduct
   on the top match.

3. EXPERT OPINIONS
   Call ScavioYouTubeSearch for "<product> review". Call
   ScavioYouTubeMetadata on the top result by view count.

4. REAL USER SENTIMENT
   Call ScavioRedditSearch for "<product> review" or "<product> worth it".
   Call ScavioRedditPost on the most relevant thread.

5. BROADER CONTEXT
   Call ScavioSearch for "<product> problems" or "<product> vs" to find
   known issues, recalls, or strong alternatives.

5. SYNTHESIZE VERDICT
   Combine all sources into this format:

   VERDICT: <BUY / SKIP / BUY WITH CAVEATS>
   ============================================================

   PRICE COMPARISON
   Amazon: $XX.XX (ASIN: <asin>) | <rating> stars (<N> reviews)
   Walmart: $XX.XX (ID: <id>) | <rating> stars (<N> reviews)
   Best price: <platform> by $XX.XX

   PROS (from reviews, Reddit, YouTube)
   - <pro 1 with source>
   - <pro 2 with source>
   - <pro 3 with source>

   CONS (from reviews, Reddit, YouTube)
   - <con 1 with source>
   - <con 2 with source>
   - <con 3 with source>

   RED FLAGS
   - <anything suspicious: fake review signals, recent recalls, known
     defects, astroturfing on Reddit>

   BOTTOM LINE
   <2-3 sentence final recommendation. State who should buy it, who
   should skip it, and the single best alternative if skipping.>

## Rules
- Never invent prices, ratings, URLs, or quotes. Only use tool output.
- If a platform returns no results for the product, note it and proceed
  with the platforms that do have data.
- Do not call every tool if the product is only sold on one platform.
  Adapt the workflow to avoid wasting credits on empty searches.
- Keep the final answer under 500 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    tools = [
        ScavioSearch(max_results=5),
        ScavioAmazonSearch(max_results=5),
        ScavioAmazonProduct(),
        ScavioWalmartSearch(max_results=5),
        ScavioWalmartProduct(),
        ScavioYouTubeSearch(max_results=5),
        ScavioYouTubeMetadata(),
        ScavioRedditSearch(max_results=5),
        ScavioRedditPost(),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(query: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


DEFAULT_QUERY = "Sony WH-1000XM5"


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    print(f"\nQuery: {query}\n{'-' * 60}")
    print(run(query))
