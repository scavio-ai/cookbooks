"""
walmart_price_logger.py -- log Walmart search prices to SQLite over time.

Runs a Walmart search and appends a timestamped price snapshot for each
result into a local SQLite database. Schedule it (cron / Task Scheduler) and
you have a price-history table for any category -- a free, self-hosted
alternative to price-tracking SaaS.

Prerequisites:
  pip install scavio python-dotenv         # sqlite3 ships with Python
  export SCAVIO_API_KEY="sk_..."

Usage:
  python walmart_price_logger.py "coffee maker" --db prices.db
  sqlite3 prices.db 'SELECT captured_at, title, price FROM snapshots ORDER BY captured_at DESC LIMIT 10;'
"""

import argparse
import sqlite3
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from scavio import ScavioClient

load_dotenv(override=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    captured_at TEXT NOT NULL,
    query       TEXT NOT NULL,
    product_id  TEXT,
    title       TEXT,
    price       REAL,
    currency    TEXT,
    rating      REAL,
    rating_count INTEGER,
    seller      TEXT
);
"""


def main():
    ap = argparse.ArgumentParser(description="Append Walmart price snapshots to SQLite.")
    ap.add_argument("query", nargs="*", default=["coffee maker"])
    ap.add_argument("--db", default="walmart_prices.db")
    ap.add_argument("--limit", type=int, default=20)
    args = ap.parse_args()

    query = " ".join(args.query) if args.query else "coffee maker"
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    products = (ScavioClient().walmart.search(query).get("data") or {}).get("products") or []
    products = products[: args.limit]

    con = sqlite3.connect(args.db)
    con.execute(SCHEMA)
    con.executemany(
        "INSERT INTO snapshots VALUES (:captured_at,:query,:product_id,:title,:price,"
        ":currency,:rating,:rating_count,:seller)",
        [
            {
                "captured_at": now,
                "query": query,
                "product_id": p.get("id"),
                "title": p.get("title"),
                "price": p.get("price"),
                "currency": p.get("currency"),
                "rating": p.get("rating"),
                "rating_count": p.get("rating_count"),
                "seller": p.get("seller_name"),
            }
            for p in products
        ],
    )
    con.commit()
    con.close()

    print(f"Logged {len(products)} '{query}' prices to {args.db} at {now}", file=sys.stderr)
    for p in products[:5]:
        print(f"  {p.get('price')} {p.get('currency') or ''}  {p.get('title')}")


if __name__ == "__main__":
    main()
