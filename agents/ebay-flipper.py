"""
EbayFlipper: AI e-commerce arbitrage finder agent.

A free alternative to Tactical Arbitrage and BuyBotPro for finding
resale opportunities. Give it a product category. It searches eBay for
deals, compares with Amazon pricing, and identifies price gaps where a
buy-low/sell-high margin exists.

Built with LangChain create_agent, OpenAI tool calling, langchain-scavio
(Amazon tools), and raw Scavio API calls (eBay endpoints).

Prerequisites:
  pip install langchain langchain-openai "langchain-scavio>=2.9" python-dotenv requests

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/ebay-flipper.py "vintage film cameras"
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioAmazonSearch

load_dotenv(override=True)

API_BASE = "https://api.scavio.dev"


def _post(path: str, body: dict) -> str:
    key = os.environ.get("SCAVIO_API_KEY")
    if not key:
        return "Error: SCAVIO_API_KEY not set -- get a free key at https://dashboard.scavio.dev"
    try:
        resp = requests.post(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=body,
            timeout=60,
        )
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_ebay_search(query: str) -> str:
    """Search eBay listings by keyword. Returns titles, prices, condition, seller."""
    return _post("/api/v1/ebay/search", {"query": query})


@tool
def scavio_ebay_product(item_id: str) -> str:
    """Get full details for an eBay item by item number or listing URL."""
    return _post("/api/v1/ebay/product", {"item_id": item_id})


SYSTEM_PROMPT = """\
You are EbayFlipper. Given a product category, find arbitrage
opportunities between eBay and Amazon.

## Workflow

1. SEARCH EBAY
   Call scavio_ebay_search with the category keyword. Note item titles,
   prices, conditions, and item ids. Focus on items priced significantly
   below what you would expect retail.

2. SEARCH AMAZON
   Call ScavioAmazonSearch with the same or similar keywords. Note
   comparable product prices on Amazon.

3. COMPARE PRICES
   For each promising eBay listing, find the closest Amazon match. A
   candidate is worth flagging when:
   - eBay price is at least 30% below the Amazon price
   - The eBay item is in "New" or "Like New" condition
   - After estimated fees (~15% eBay + ~15% Amazon), there is still
     margin

4. EXAMINE BEST CANDIDATES
   Call scavio_ebay_product on the top 2-3 eBay deals for more details:
   seller rating, shipping cost, return policy.

5. SYNTHESIZE AND ANSWER
   Return a list of up to 5 arbitrage candidates:

   #N  <eBay item title>
   eBay: $<price> (<condition>) -- Item #<id>
   Amazon comparable: $<price>
   Est. margin after fees: $<amount> (~<percent>%)
   Risk: <one line -- seller rating, return policy, shipping>

   End with one line of advice on the category's flip potential.

## Rules
- Only list items whose prices came from actual API responses.
- Do not fabricate Amazon prices; if no close match exists, skip.
- Account for ~30% combined platform fees in margin calculations.
- Keep the final answer under 350 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [
        scavio_ebay_search,
        scavio_ebay_product,
        ScavioAmazonSearch(max_results=10),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(category: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": category}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "vintage film cameras"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nCategory: {brief}\n{'-' * 60}")
    print(run(brief))
