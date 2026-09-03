"""
Target product reviews scraper -- pure Scavio API scraper.

Scrapes data straight from the Scavio API endpoint POST /api/v1/target/reviews.
No SDK, no framework -- just `requests`. Returns the raw JSON the API gives back.

------------------------------------------------------------------------------
 Powered by Scavio (https://scavio.dev) -- the real-time search API for AI agents.
Get a free API key (50 free credits, no credit card): https://dashboard.scavio.dev
Docs: https://scavio.dev/docs
------------------------------------------------------------------------------

Prerequisites:
  pip install requests
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev

Usage:
  python target_reviews_scraper.py "1010453160"
"""

import json
import os
import sys

import requests

API_URL = "https://api.scavio.dev/api/v1/target/reviews"


def scrape(tcin: str) -> dict:
    api_key = os.environ.get("SCAVIO_API_KEY")
    if not api_key:
        raise SystemExit("Set SCAVIO_API_KEY -- get a free key at https://dashboard.scavio.dev")
    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"tcin": tcin},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python target_reviews_scraper.py '1010453160'", file=sys.stderr)
        raise SystemExit(1)
    tcin = sys.argv[1]
    data = scrape(tcin)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print(
        "\nScraped with Scavio -- https://scavio.dev | "
        "Free API key: https://dashboard.scavio.dev",
        file=sys.stderr,
    )
