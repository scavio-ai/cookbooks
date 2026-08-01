"""
amazon_bulk_catalog.py -- turn a list of ASINs into a product CSV catalog.

Feed it ASINs (args, a file, or stdin); it pulls full product detail for each
and writes a tidy CSV: asin, title, brand, price, currency, rating, reviews,
buy-box seller. The backbone of any catalog sync, repricer, or arbitrage sheet.

Wire quirk handled for you: the product endpoint takes the ASIN in the
"query" field; the SDK exposes it cleanly as client.amazon.product(asin).

`price` is the buy-box price and `sold_by` is the seller holding it. The old
`buybox[]` array is gone; for every competing seller on an ASIN (price,
condition, shipping, who owns the buy box) call client.amazon.offers(asin).

Prerequisites:
  pip install scavio python-dotenv
  export SCAVIO_API_KEY="sk_..."

Usage:
  python amazon_bulk_catalog.py B0C7SFV8RH B01LP0U5X0 --out catalog.csv
  printf 'B0C7SFV8RH\nB01LP0U5X0\n' | python amazon_bulk_catalog.py --out catalog.csv
"""

import argparse
import csv
import sys

from dotenv import load_dotenv
from scavio import ScavioClient

load_dotenv(override=True)

FIELDS = [
    "asin",
    "title",
    "brand",
    "price",
    "list_price",
    "currency",
    "rating",
    "reviews_count",
    "seller",
    "has_buy_box",
    "availability",
]


def snapshot(client: ScavioClient, asin: str) -> dict:
    data = client.amazon.product(asin).get("data", {})
    return {
        "asin": data.get("asin") or asin,
        "title": data.get("title"),
        "brand": data.get("brand"),
        "price": data.get("price"),
        "list_price": data.get("list_price"),
        "currency": data.get("currency"),
        "rating": data.get("rating"),
        "reviews_count": data.get("reviews_count"),
        "seller": data.get("sold_by"),
        "has_buy_box": data.get("has_buy_box"),
        "availability": data.get("availability"),
    }


def read_asins(args) -> list:
    if args.asins:
        return args.asins
    return [line.strip() for line in sys.stdin if line.strip()]


def main():
    ap = argparse.ArgumentParser(description="Bulk Amazon ASIN -> product CSV.")
    ap.add_argument("asins", nargs="*", help="ASINs (or pipe them on stdin)")
    ap.add_argument("--out", default="amazon_catalog.csv")
    args = ap.parse_args()

    asins = read_asins(args) or ["B0C7SFV8RH", "B01LP0U5X0"]
    client = ScavioClient()

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for asin in asins:
            row = snapshot(client, asin)
            writer.writerow(row)
            print(f"  {row['asin']}  {row['price']} {row['currency'] or ''}  {row['title']}", file=sys.stderr)

    print(f"Wrote {len(asins)} products to {args.out}")


if __name__ == "__main__":
    main()
