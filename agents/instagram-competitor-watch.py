"""
InstagramCompetitorWatch: track what competitor brands post on Instagram.

A free alternative to social-listening suites for Instagram competitive intel.
Give it one or more competitor handles. It pulls each profile plus their recent
posts and reels with the Scavio Python SDK, trims them to the fields that
matter, and asks an LLM to report posting cadence, the best-performing recent
content, and the themes/formats they lean on.

This recipe uses the SDK directly (not a tool-calling agent) because raw
Instagram payloads are large -- fetch, trim, then reason. A clean pattern for
any high-volume social source.

Prerequisites:
  pip install scavio langchain-openai python-dotenv
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/instagram-competitor-watch.py ouraring whoop
"""

import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from scavio import ScavioClient

load_dotenv(override=True)


def trim_media(items):
    """Keep only the engagement-relevant fields from a post/reel list."""
    out = []
    for it in items or []:
        out.append(
            {
                "likes": it.get("like_count"),
                "comments": it.get("comment_count"),
                "views": it.get("view_count"),
                "is_video": it.get("is_video"),
                "caption": (it.get("caption_text") or "")[:200],
            }
        )
    return out


def gather(client: ScavioClient, handle: str) -> dict:
    profile = client.instagram.profile(username=handle).get("data") or {}
    posts = (client.instagram.user_posts(username=handle, count=12).get("data") or {}).get("items")
    reels = (client.instagram.user_reels(username=handle, count=12).get("data") or {}).get("items")
    return {
        "handle": handle,
        "followers": profile.get("follower_count"),
        "bio": profile.get("biography"),
        "category": profile.get("category"),
        "recent_posts": trim_media(posts),
        "recent_reels": trim_media(reels),
    }


PROMPT = """You are InstagramCompetitorWatch. Below is trimmed data for one or
more competitor Instagram accounts (profile + recent posts and reels with
engagement metrics).

For each account, report:
  @handle  --  <followers> followers
  Cadence: post vs reel mix and rough activity level
  Top content: 2-3 standouts, each with the metric that flags it
  Themes/formats: bullets drawn from captions
  Takeaway: one thing to test

Use only the data provided. Never invent metrics or captions. Keep it under
450 words.

DATA:
{data}
"""


def run(handles: list) -> str:
    client = ScavioClient()
    data = [gather(client, h.lstrip("@")) for h in handles]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    import json

    return llm.invoke(PROMPT.format(data=json.dumps(data, ensure_ascii=False, indent=1))).content


if __name__ == "__main__":
    handles = sys.argv[1:] or ["ouraring", "whoop"]
    print(f"\nCompetitors: {', '.join(handles)}\n{'-' * 60}")
    print(run(handles))
