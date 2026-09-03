"""
YelpReputationMonitor: AI local-business reputation tracking agent.

A free alternative to Birdeye, Podium, and ReviewTrackers for local
business reputation analysis. Give it a business type and location.
It searches Yelp, reads business details and reviews for top results,
and returns a reputation report: rating distribution, common praise
and complaints, owner response rate, and competitive positioning.

Built with LangChain create_agent, OpenAI tool calling, and custom
Scavio API tools for Yelp data.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Get a free Scavio API key (50 free credits, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/yelp-reputation-monitor.py "coffee shops in Austin, TX"
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

API_BASE = "https://api.scavio.dev"


def _headers():
    key = os.environ.get("SCAVIO_API_KEY", "")
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def _post(path: str, body: dict) -> str:
    if not os.environ.get("SCAVIO_API_KEY"):
        return "Error: SCAVIO_API_KEY not set -- get a free key at https://dashboard.scavio.dev"
    try:
        resp = requests.post(f"{API_BASE}{path}", headers=_headers(), json=body, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_yelp_search(term: str, location: str) -> str:
    """Search Yelp businesses by term and location. Returns ranked results with rating, review count, price band, categories, and address."""
    return _post("/api/v1/yelp/search", {"term": term, "location": location})


@tool
def scavio_yelp_business(business_id: str) -> str:
    """Get full Yelp business details by business_id or alias: rating histogram, review count, hours, amenities, photos, and the first page of reviews."""
    return _post("/api/v1/yelp/business", {"business_id": business_id})


@tool
def scavio_yelp_reviews(business_id: str, page: int = 1) -> str:
    """Get a page of Yelp reviews for a business. Each review has rating, text, author, date, photos, and any owner response."""
    return _post("/api/v1/yelp/reviews", {"business_id": business_id, "page": page})


SYSTEM_PROMPT = """You are YelpReputationMonitor. Given a business type and \
location, produce a competitive reputation report from real Yelp data.

## Workflow

1. SEARCH
   Call scavio_yelp_search with the business type as term and the city as
   location. Note the top 5 results by rating and review count.

2. DEEP READ (pick top 3)
   For the 3 most relevant results, call scavio_yelp_business to get the
   rating histogram, amenities, hours, and embedded first-page reviews.
   If a business has 50+ reviews, call scavio_yelp_reviews page=1 to read
   recent sentiment.

3. ANALYZE
   From the data, identify:
   - Rating distribution across the competitive set (how many at 4+, 3.5, etc.)
   - Common praise themes (words/phrases that recur in positive reviews)
   - Common complaint themes (recurring in negative reviews)
   - Owner response rate (how many reviews have an owner reply)
   - Competitive positioning: who leads on what (best rated, most reviewed,
     best hours, unique amenities)

4. REPORT
   Return a structured reputation report:

   MARKET: <location> -- <business type>
   Businesses analyzed: <N>

   COMPETITIVE LANDSCAPE
   #1 <name> -- <rating> (<review_count> reviews) -- <one-line positioning>
   #2 ...
   #3 ...

   RATING DISTRIBUTION
   <summary of how ratings cluster across the set>

   WHAT CUSTOMERS PRAISE
   - <theme 1>
   - <theme 2>

   WHAT CUSTOMERS COMPLAIN ABOUT
   - <theme 1>
   - <theme 2>

   OWNER ENGAGEMENT
   <who responds to reviews and how often>

   OPPORTUNITY
   <one paragraph: what an operator in this market should focus on>

## Rules
- Only report data from actual Yelp results. Never invent business names,
  ratings, review text, or counts.
- Keep the final answer under 500 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_yelp_search, scavio_yelp_business, scavio_yelp_reviews]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "coffee shops in Austin, TX"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
