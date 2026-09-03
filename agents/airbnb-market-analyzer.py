"""
AirbnbMarketAnalyzer: AI short-term rental market analysis agent.

A free alternative to AirDNA and Mashvisor for analyzing short-term
rental markets. Give it a location. It searches Airbnb listings,
examines pricing and amenities of top listings, reads guest reviews,
and returns a market brief: median nightly rate, occupancy signals,
must-have amenities, and guest complaints to avoid.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
Airbnb API via custom tools.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/airbnb-market-analyzer.py "Austin, TX"
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
def scavio_airbnb_search(location: str) -> str:
    """Search Airbnb listings in a location: prices, ratings, property types, amenities."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/airbnb/search", headers=HEADERS(), json={"location": location}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_airbnb_listing(listing_id: str) -> str:
    """Fetch full details for one Airbnb listing: amenities, pricing, house rules, host info."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/airbnb/listing", headers=HEADERS(), json={"listing_id": listing_id}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


@tool
def scavio_airbnb_reviews(listing_id: str) -> str:
    """Fetch guest reviews for an Airbnb listing: rating, text, date."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/airbnb/reviews", headers=HEADERS(), json={"listing_id": listing_id}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


SYSTEM_PROMPT = """\
You are AirbnbMarketAnalyzer. Given a location, produce a short-term \
rental market analysis for someone considering investing in or listing \
a property there.

## Workflow

1. SEARCH
   Call scavio_airbnb_search with the location. Note the property
   types, nightly prices, ratings, and review counts across results.

2. LISTING DEEP DIVE
   Pick the top 1-2 highest-rated listings from search. Call
   scavio_airbnb_listing on each. Note: amenities, pricing details,
   property type, bedrooms/bathrooms, host details, Superhost status.

3. GUEST SENTIMENT
   Call scavio_airbnb_reviews on the best-reviewed listing. Read
   reviews to identify what guests praise and complain about.

4. REPORT
   Return:

   MARKET: <location>

   PRICING
   Nightly range: $<low> - $<high>
   Median nightly rate: ~$<estimate>
   Typical property: <bedrooms/type>

   SUPPLY SNAPSHOT
   Listings found: <N>
   Superhost %: <rough estimate from results>
   Avg rating: <N>/5

   MUST-HAVE AMENITIES
   - <top amenities from successful listings: wifi, kitchen, etc.>

   WHAT GUESTS LOVE
   - <themes from positive reviews>

   WHAT GUESTS COMPLAIN ABOUT
   - <themes from negative reviews -- these are your edge>

   COMPETITIVE POSITIONING
   - <what a new listing needs to stand out in this market>

   VERDICT: <2-3 sentences on market attractiveness and entry strategy>

## Rules
- Only report data from tool results. Never invent prices or ratings.
- Keep under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_airbnb_search, scavio_airbnb_listing, scavio_airbnb_reviews]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(location: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": f"Analyze the short-term rental market in: {location}"}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "Austin, TX"


if __name__ == "__main__":
    location = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nLocation: {location}\n{'-' * 60}")
    print(run(location))
