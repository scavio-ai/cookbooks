"""
tiktok_hashtag_trend_logger.py -- log TikTok hashtag reach to SQLite over time.

Resolves a hashtag to its TikTok challenge and appends a timestamped snapshot
of its video count and view count to SQLite. Run it daily and you can chart a
hashtag's momentum -- is a trend accelerating or cooling? A free alternative
to paid TikTok trend dashboards.

Prerequisites:
  pip install scavio python-dotenv
  export SCAVIO_API_KEY="sk_..."

Usage:
  python tiktok_hashtag_trend_logger.py coffee booktok --db tiktok_trends.db
  sqlite3 tiktok_trends.db 'SELECT captured_at, hashtag, video_count, view_count FROM trends;'
"""

import argparse
import sqlite3
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from scavio import ScavioClient

load_dotenv(override=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS trends (
    captured_at TEXT NOT NULL,
    hashtag     TEXT NOT NULL,
    hashtag_id  TEXT,
    video_count INTEGER,
    view_count  INTEGER
);
"""


def snapshot(client: ScavioClient, name: str) -> dict:
    info = (client.tiktok.hashtag(hashtag_name=name).get("data") or {}).get("challengeInfo") or {}
    stats = info.get("stats") or {}
    challenge = info.get("challenge") or {}
    return {
        "hashtag": name,
        "hashtag_id": challenge.get("id"),
        "video_count": stats.get("videoCount"),
        "view_count": stats.get("viewCount"),
    }


def main():
    ap = argparse.ArgumentParser(description="Append TikTok hashtag reach snapshots to SQLite.")
    ap.add_argument("hashtags", nargs="*", default=["coffee"])
    ap.add_argument("--db", default="tiktok_trends.db")
    args = ap.parse_args()

    hashtags = args.hashtags or ["coffee"]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    con = sqlite3.connect(args.db)
    con.execute(SCHEMA)
    client = ScavioClient()
    for name in hashtags:
        snap = snapshot(client, name.lstrip("#"))
        con.execute(
            "INSERT INTO trends VALUES (?,?,?,?,?)",
            (now, snap["hashtag"], snap["hashtag_id"], snap["video_count"], snap["view_count"]),
        )
        print(f"  #{snap['hashtag']}  videos={snap['video_count']}  views={snap['view_count']}", file=sys.stderr)
    con.commit()
    con.close()
    print(f"Logged {len(hashtags)} hashtag(s) to {args.db} at {now}")


if __name__ == "__main__":
    main()
