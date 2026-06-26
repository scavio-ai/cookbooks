"""
YouTube video metadata scraper -- pure Scavio API scraper.

Scrapes full metadata for a YouTube video -- views, likes, comments, duration, channel,
straight from the Scavio API endpoint POST /api/v1/youtube/metadata. No SDK, no
framework -- just `requests`. Returns the raw JSON the API gives back.

------------------------------------------------------------------------------
 Powered by Scavio (https://scavio.dev) -- one real-time search API for Google,
 YouTube, Amazon, Walmart, Reddit, TikTok, and Instagram.
 Get a free API key (50 free credits, no credit card): https://dashboard.scavio.dev
 Docs: https://scavio.dev/docs
------------------------------------------------------------------------------

Prerequisites:
  pip install requests
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev

Usage:
  python youtube_video_scraper.py "dQw4w9WgXcQ"
"""

import json
import os
import sys

import requests

API_URL = "https://api.scavio.dev/api/v1/youtube/metadata"


def scrape(video_id: str) -> dict:
    api_key = os.environ.get("SCAVIO_API_KEY")
    if not api_key:
        raise SystemExit("Set SCAVIO_API_KEY -- get a free key at https://dashboard.scavio.dev")
    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"video_id": video_id},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_video_scraper.py <video_id>", file=sys.stderr)
        raise SystemExit(1)
    video_id = sys.argv[1]
    data = scrape(video_id)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print(
        "\nScraped with Scavio -- https://scavio.dev | "
        "Free API key: https://dashboard.scavio.dev",
        file=sys.stderr,
    )
