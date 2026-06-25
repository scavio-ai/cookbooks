"""
Amazon product scraper -- pure Scavio API scraper.

Scrapes full Amazon product detail for an ASIN (the ASIN goes in the `query` field),
straight from the Scavio API endpoint POST /api/v1/amazon/product. No SDK, no
framework -- just `requests`. Returns the raw JSON the API gives back.

------------------------------------------------------------------------------
 Powered by Scavio (https://scavio.dev) -- one real-time search API for Google,
 YouTube, Amazon, Walmart, Reddit, TikTok, and Instagram.
 Get a free API key (250 credits/month, no credit card): https://dashboard.scavio.dev
 Docs: https://scavio.dev/docs
------------------------------------------------------------------------------

Prerequisites:
  pip install requests
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev

Usage:
  python amazon_product_scraper.py "B0C7SFV8RH"
"""

import json
import os
import sys

import requests

API_URL = "https://api.scavio.dev/api/v1/amazon/product"


def scrape(asin: str) -> dict:
    api_key = os.environ.get("SCAVIO_API_KEY")
    if not api_key:
        raise SystemExit("Set SCAVIO_API_KEY -- get a free key at https://dashboard.scavio.dev")
    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"query": asin},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python amazon_product_scraper.py <asin>", file=sys.stderr)
        raise SystemExit(1)
    asin = sys.argv[1]
    data = scrape(asin)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print(
        "\nScraped with Scavio -- https://scavio.dev | "
        "Free API key: https://dashboard.scavio.dev",
        file=sys.stderr,
    )
