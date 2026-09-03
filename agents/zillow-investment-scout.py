"""
ZillowInvestmentScout: AI real estate investment analysis agent.

A free alternative to Mashvisor, Roofstock, and DealCheck for sizing up a
rental market. Give it a city or metro. It searches Zillow listings, examines
individual properties, and pulls Redfin market data for price trends --
then returns a concise investment brief.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
real-time search API (Zillow + Redfin endpoints).

Prerequisites:
  pip install langchain langchain-openai python-dotenv requests

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/zillow-investment-scout.py "Austin, TX"
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
HEADERS = lambda: {
    "Authorization": f"Bearer {os.environ.get('SCAVIO_API_KEY', '')}",
    "Content-Type": "application/json",
}


def _post(path: str, body: dict) -> str:
    key = os.environ.get("SCAVIO_API_KEY")
    if not key:
        return "Error: SCAVIO_API_KEY not set -- get a free key at https://dashboard.scavio.dev"
    try:
        resp = requests.post(f"{API_BASE}{path}", headers=HEADERS(), json=body, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_zillow_search(location: str) -> str:
    """Search Zillow property listings for a city, ZIP, or region slug like 'austin-tx'."""
    return _post("/api/v1/zillow/search", {"location": location})


@tool
def scavio_zillow_property(zpid: str) -> str:
    """Get full details for a Zillow property by its zpid or listing URL."""
    return _post("/api/v1/zillow/property", {"zpid": zpid})


@tool
def scavio_redfin_market(location: str) -> str:
    """Get Redfin market data (median price, trends, inventory) for a city or region."""
    return _post("/api/v1/redfin/market", {"location": location})


SYSTEM_PROMPT = """\
You are ZillowInvestmentScout. Given a city or market, produce a concise
real estate investment brief.

## Workflow

1. SEARCH LISTINGS
   Call scavio_zillow_search with the market name. Note the price range,
   property types, and neighborhoods that appear.

2. EXAMINE TOP LISTINGS
   Pick 2-3 interesting listings (varied price/type). Call
   scavio_zillow_property on each to get details: price, beds/baths,
   Zestimate, rent Zestimate, tax, HOA, year built, lot size.

3. MARKET CONTEXT
   Call scavio_redfin_market for the same area. Note median sale price,
   month-over-month and year-over-year trends, inventory, days on market.

4. SYNTHESIZE AND ANSWER
   Return a brief with these sections:

   MARKET SNAPSHOT
   - Median list price (from Zillow search)
   - Median sale price + YoY change (from Redfin)
   - Days on market, inventory level

   PRICE-TO-RENT SIGNALS
   - For examined listings: price vs rent Zestimate, gross yield %
   - Flag any listing where gross yield > 8% as worth a deeper look

   NEIGHBORHOODS TO WATCH
   - 2-3 neighborhoods from the search with the best price/rent ratio
     or the steepest discount to Zestimate

   MARKET DIRECTION
   - One paragraph: is this market heating, cooling, or flat? Support
     with the Redfin trend data.

## Rules
- Only cite numbers that actually appeared in API responses.
- If rent Zestimate is missing, say so -- do not fabricate yields.
- Keep the final answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_zillow_search, scavio_zillow_property, scavio_redfin_market]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(market: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": market}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "Austin, TX"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nMarket: {brief}\n{'-' * 60}")
    print(run(brief))
