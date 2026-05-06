"""
PriceWar: Amazon vs Walmart arbitrage finder.

Give it a product keyword. It searches both Amazon and Walmart, matches
products across platforms, calculates price deltas and margins, and
surfaces the best arbitrage opportunities for resellers and dropshippers.

Prerequisites:
  pip install langchain langchain-openai langchain-scavio python-dotenv

  Get a free Scavio API key (500 credits/month, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/pricewar.py "wireless earbuds"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import (
    ScavioAmazonProduct,
    ScavioAmazonSearch,
    ScavioWalmartProduct,
    ScavioWalmartSearch,
)

load_dotenv(override=True)


SYSTEM_PROMPT = """You are PriceWar, a cross-platform arbitrage analyst for \
Amazon and Walmart.

## Workflow

1. SEARCH BOTH PLATFORMS
   First call ScavioAmazonSearch with the user's product keyword.
   Then, in a SEPARATE step, call ScavioWalmartSearch with the same
   keyword. Do NOT call both search tools in the same turn -- the API
   rate-limits concurrent requests.

2. MATCH PRODUCTS
   Compare results across platforms by product name, brand, and model
   number. Identify products that appear on both Amazon and Walmart.
   Also note products that appear on only one platform -- these may be
   exclusive listings worth investigating.

3. PULL DETAILS
   For the top 3 matched products with the largest apparent price
   difference, call ScavioAmazonProduct and ScavioWalmartProduct to get
   full pricing, ratings, and availability.

4. CALCULATE MARGINS
   For each matched product, compute:
   - Price delta: absolute difference between platforms
   - Gross margin: (higher price - lower price) / higher price * 100
   - Direction: which platform is cheaper (buy) vs more expensive (sell)
   Assume 15% marketplace seller fees on the selling platform.
   Net margin = gross margin - 15%.

5. OUTPUT
   Return a ranked table of arbitrage opportunities, best margin first:

   ARBITRAGE OPPORTUNITIES: "<keyword>"
   ============================================================

   #1  <Product Name>
       Amazon: $XX.XX (ASIN: <asin>) | <rating> stars, <N> reviews
       Walmart: $XX.XX (ID: <id>) | <rating> stars, <N> reviews
       Delta: $XX.XX | Gross Margin: XX% | Net Margin (after 15% fees): XX%
       Direction: Buy on <platform>, sell on <platform>
       Risk: <one-line risk factor: low review count, price volatility, etc.>

   Repeat for up to 5 opportunities.

   End with a SUMMARY line: "X opportunities found. Best net margin: XX%
   on <product>. Minimum viable margin (>15% net) met by X products."

## Rules
- Never invent prices, ASINs, product IDs, ratings, or review counts.
- Only report matches where you have confirmed data from both platforms.
- If no cross-platform matches are found, say so and list the best
  single-platform deals instead.
- Keep the final answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    tools = [
        ScavioAmazonSearch(max_results=5),
        ScavioWalmartSearch(max_results=5),
        ScavioAmazonProduct(),
        ScavioWalmartProduct(),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(query: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


DEFAULT_QUERY = "wireless earbuds"


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    print(f"\nQuery: {query}\n{'-' * 60}")
    print(run(query))
