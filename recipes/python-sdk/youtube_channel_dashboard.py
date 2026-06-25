"""
youtube_channel_dashboard.py -- rank a topic's top videos by real engagement.

Searches YouTube for a topic, takes the top N videos, enriches each with full
metadata (views, likes, comments), computes an engagement rate, and prints a
sorted dashboard table. Search snippets only give fuzzy "1.2M views" text --
this resolves the real numbers via the metadata endpoint.

Prerequisites:
  pip install scavio python-dotenv
  export SCAVIO_API_KEY="sk_..."

Cost: 1 credit for the search + 1 per video enriched (default 5).

Usage:
  python youtube_channel_dashboard.py "langchain agents tutorial" --top 5
"""

import argparse
import sys

from dotenv import load_dotenv
from scavio import ScavioClient

load_dotenv(override=True)


def main():
    ap = argparse.ArgumentParser(description="Build a YouTube engagement dashboard for a topic.")
    ap.add_argument("topic", nargs="*", default=["langchain agents tutorial"])
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    topic = " ".join(args.topic) if args.topic else "langchain agents tutorial"
    client = ScavioClient()

    results = (client.youtube.search(topic, sort_by="view_count").get("data") or {}).get("results") or []
    video_ids = [r.get("videoId") for r in results if r.get("videoId")][: args.top]

    rows = []
    for vid in video_ids:
        m = client.youtube.metadata(vid).get("data") or {}
        views = m.get("view_count") or 0
        likes = m.get("like_count") or 0
        comments = m.get("comment_count") or 0
        engagement = round(100 * (likes + comments) / views, 2) if views else 0.0
        rows.append((views, likes, comments, engagement, m.get("uploader"), m.get("title")))

    rows.sort(reverse=True)  # by views desc
    print(f"\nTopic: {topic}\n")
    print(f"{'VIEWS':>12}  {'LIKES':>9}  {'COMMENTS':>8}  {'ENG%':>5}  CHANNEL / TITLE")
    print("-" * 90)
    for views, likes, comments, eng, channel, title in rows:
        print(f"{views:>12,}  {likes:>9,}  {comments:>8,}  {eng:>5}  {channel} -- {title[:55]}")

    if not rows:
        print("No videos found.", file=sys.stderr)


if __name__ == "__main__":
    main()
