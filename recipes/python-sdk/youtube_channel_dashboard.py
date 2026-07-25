"""
youtube_channel_dashboard.py -- a channel's top videos ranked by real views.

Resolves a channel (id, @handle, or URL), prints its headline stats
(subscribers, total videos, lifetime views), then lists its videos ranked by
view count. The channel and channel/videos endpoints return real integer
counts, so no fuzzy "1.2M views" text parsing is needed.

Prerequisites:
  pip install scavio python-dotenv
  export SCAVIO_API_KEY="sk_..."

Cost: 1 credit for the channel lookup + 1 for the video list.

Usage:
  python youtube_channel_dashboard.py "@LangChain" --top 10
"""

import argparse
import sys

from dotenv import load_dotenv
from scavio import ScavioClient

load_dotenv(override=True)


def main():
    ap = argparse.ArgumentParser(description="Build a YouTube dashboard for a channel.")
    ap.add_argument("channel", nargs="*", default=["@LangChain"])
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()

    channel = " ".join(args.channel) if args.channel else "@LangChain"
    client = ScavioClient()

    info = client.youtube.channel(channel).get("data") or {}
    channel_id = info.get("channel_id")
    if not channel_id:
        print(f"Could not resolve channel: {channel}", file=sys.stderr)
        raise SystemExit(1)

    videos = (client.youtube.channel_videos(channel_id).get("data") or {}).get("results") or []
    videos.sort(key=lambda v: v.get("view_count") or 0, reverse=True)
    videos = videos[: args.top]

    print(f"\nChannel: {info.get('title')}  ({channel_id})")
    print(
        f"Subscribers: {info.get('subscriber_count') or 0:,}  |  "
        f"Videos: {info.get('video_count') or 0:,}  |  "
        f"Lifetime views: {info.get('view_count') or 0:,}\n"
    )
    print(f"{'VIEWS':>14}  {'PUBLISHED':<14}  {'LEN':>8}  TITLE")
    print("-" * 90)
    for v in videos:
        views = v.get("view_count") or 0
        published = (v.get("published_time") or "")[:14]
        length = v.get("duration_text") or ""
        title = (v.get("title") or "")[:52]
        print(f"{views:>14,}  {published:<14}  {length:>8}  {title}")

    if not videos:
        print("No videos found.", file=sys.stderr)


if __name__ == "__main__":
    main()
