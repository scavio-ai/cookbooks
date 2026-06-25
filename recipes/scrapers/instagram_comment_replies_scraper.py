"""
Instagram comment replies scraper -- pure Scavio API scraper.

Scrapes replies to a specific comment on an Instagram post,
straight from the Scavio API endpoint POST /api/v1/instagram/post/comments/replies. No SDK, no
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
  python instagram_comment_replies_scraper.py "3920738671208852726" "18093"
"""

import json
import os
import sys

import requests

API_URL = "https://api.scavio.dev/api/v1/instagram/post/comments/replies"


def scrape(media_id: str, comment_id: str) -> dict:
    api_key = os.environ.get("SCAVIO_API_KEY")
    if not api_key:
        raise SystemExit("Set SCAVIO_API_KEY -- get a free key at https://dashboard.scavio.dev")
    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"media_id": media_id, "comment_id": comment_id},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python instagram_comment_replies_scraper.py <media_id> <comment_id>", file=sys.stderr)
        raise SystemExit(1)
    media_id = sys.argv[1]
    comment_id = sys.argv[2]
    data = scrape(media_id, comment_id)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print(
        "\nScraped with Scavio -- https://scavio.dev | "
        "Free API key: https://dashboard.scavio.dev",
        file=sys.stderr,
    )
