"""
EtsyMarketResearcher: AI market analysis agent for Etsy niches.

A free alternative to eRank, Marmalead, and Sale Samurai for
researching handmade and vintage product niches on Etsy. Give it a
product niche. It searches listings, examines top products and shops,
reads reviews, and returns a market brief: price range, top sellers,
customer sentiment themes, and gap opportunities.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
Etsy API via custom tools.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/etsy-market-researcher.py "handmade ceramic mugs"
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


def _check_key() -> str | None:
    if not os.environ.get("SCAVIO_API_KEY"):
        return "Error: SCAVIO_API_KEY not set -- get a free key at https://dashboard.scavio.dev"
    return None


@tool
def scavio_etsy_search(query: str) -> str:
    """Search Etsy listings: title, price, shop, rating, review count."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/etsy/search", headers=HEADERS(), json={"query": query}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_etsy_product(listing: str) -> str:
    """Fetch full details for one Etsy listing: description, price, materials, variations, reviews."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/etsy/product", headers=HEADERS(), json={"listing": listing}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


@tool
def scavio_etsy_shop(shop: str) -> str:
    """Fetch an Etsy shop profile: sales count, rating, star seller status, about."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/etsy/shop", headers=HEADERS(), json={"shop": shop}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:4000]


@tool
def scavio_etsy_reviews(shop: str) -> str:
    """Fetch reviews for an Etsy shop across all its listings."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/etsy/reviews", headers=HEADERS(), json={"shop": shop}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


SYSTEM_PROMPT = """\
You are EtsyMarketResearcher. Given a product niche, produce a market \
analysis brief for someone considering selling in that niche on Etsy.

## Workflow

1. SEARCH
   Call scavio_etsy_search with the niche query. Note the price range,
   review counts, and shop names across results. Identify the top 3
   listings by review count or apparent sales volume.

2. PRODUCT DEEP DIVE
   Call scavio_etsy_product on the top 1-2 listings. Note: price,
   description keywords, materials, shipping info, and the first
   reviews.

3. SHOP ANALYSIS
   Pick the most successful shop from search results. Call
   scavio_etsy_shop to get sales count, rating, and star seller
   status.

4. REVIEW SENTIMENT
   Call scavio_etsy_reviews on that shop. Read the reviews to identify
   what customers praise and complain about.

5. REPORT
   Return:

   NICHE: <niche>

   MARKET SNAPSHOT
   Price range: $<low> - $<high> (median ~$<mid>)
   Listings found: <N>
   Competition level: <low / moderate / high>

   TOP SELLERS
   #1: <shop name> -- <sales> sales, <rating> stars, Star Seller: <yes/no>
   #2: ...

   WHAT SELLS
   - <common product traits: materials, styles, price points>

   CUSTOMER SENTIMENT
   Praise: <what buyers love>
   Complaints: <what buyers dislike or wish was different>

   GAP OPPORTUNITIES
   - <underserved angles: missing styles, price gaps, shipping issues
     competitors have that you could avoid>

   VERDICT: <2-3 sentences on whether this niche is worth entering>

## Rules
- Only report data from tool results. Never invent shop names or prices.
- Keep under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_etsy_search, scavio_etsy_product, scavio_etsy_shop, scavio_etsy_reviews]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(niche: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": f"Analyze this Etsy niche: {niche}"}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "handmade ceramic mugs"


if __name__ == "__main__":
    niche = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nNiche: {niche}\n{'-' * 60}")
    print(run(niche))
