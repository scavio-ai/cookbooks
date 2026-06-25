"""
reddit_alert_watcher.py -- alert on new Reddit posts matching a keyword.

Searches Reddit "new" for one or more keywords and prints any post it has not
seen before, persisting seen ids to a small JSON state file. Run it on a
schedule for brand monitoring or lead-gen -- a free alternative to F5Bot and
GummySearch. The print loop is a clean hook point for Slack/email/webhook.

Reddit search costs 2 credits per keyword per run.

Prerequisites:
  pip install scavio python-dotenv
  export SCAVIO_API_KEY="sk_..."

Usage:
  python reddit_alert_watcher.py "serpapi alternative" "amazon product api"
"""

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from scavio import ScavioClient

load_dotenv(override=True)


def load_state(path: Path) -> set:
    if path.exists():
        return set(json.loads(path.read_text()))
    return set()


def save_state(path: Path, seen: set) -> None:
    path.write_text(json.dumps(sorted(seen)))


def notify(post: dict) -> None:
    # Replace this with a Slack/Discord webhook or email send.
    print(
        f"NEW  r/{post.get('subreddit')}  by u/{post.get('author')}\n"
        f"  {post.get('title')}\n  {post.get('url')}\n"
    )


def main():
    ap = argparse.ArgumentParser(description="Alert on new Reddit posts for keywords.")
    ap.add_argument("keywords", nargs="*", default=["serpapi alternative"])
    ap.add_argument("--state", default=".reddit_seen.json")
    args = ap.parse_args()

    keywords = args.keywords or ["serpapi alternative"]
    state_path = Path(args.state)
    seen = load_state(state_path)

    client = ScavioClient()
    new_count = 0
    for kw in keywords:
        posts = (client.reddit.search(kw, sort="new").get("data") or {}).get("posts") or []
        for post in posts:
            pid = post.get("id")
            if pid and pid not in seen:
                seen.add(pid)
                notify(post)
                new_count += 1

    save_state(state_path, seen)
    print(f"{new_count} new post(s); tracking {len(seen)} seen ids in {state_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
