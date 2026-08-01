#!/usr/bin/env bash
#
# amazon-price-snapshot.sh -- Amazon search to a price snapshot table.
#
# Searches Amazon for a keyword, then pulls full product detail for the top
# ASIN (price, rating, buy-box seller, availability) -- the two-call pattern
# every price tracker or arbitrage tool is built on. A free alternative to
# Keepa and Jungle Scout for ad-hoc checks.
#
# Two wire quirks:
#   - the product endpoint takes the ASIN in the "query" field, not "asin";
#   - search results are NOT ranked. The upstream ignores every sort value, so
#     there is no "top organic" row to trust -- pick deliberately (cheapest
#     priced non-sponsored match below) rather than taking index 0.
#
# Requires: curl, jq, SCAVIO_API_KEY (https://dashboard.scavio.dev).
#
# Usage:
#   ./amazon-price-snapshot.sh "yoga mat"
#
set -euo pipefail

: "${SCAVIO_API_KEY:?Set SCAVIO_API_KEY (https://dashboard.scavio.dev)}"
QUERY="${*:-yoga mat}"
API="https://api.scavio.dev/api/v1"
AUTH="Authorization: Bearer ${SCAVIO_API_KEY}"

echo "Searching Amazon for: ${QUERY}" >&2

# 5 cheapest non-sponsored priced results, deduped by ASIN. `price` is a
# number, so sorting on it needs no string cleaning.
SEARCH=$(curl -sS -X POST "${API}/amazon/search" -H "$AUTH" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg q "$QUERY" '{query:$q}')")

echo "$SEARCH" | jq -r '
  .data.products
  | map(select((.is_sponsored | not) and (.price != null)))
  | unique_by(.asin) | sort_by(.price) | .[:5][]
  | [.asin, .price, (.currency // ""), (.rating // "n/a"), (.reviews_count // 0), (.badge // ""), .title]
  | @tsv' \
| column -t -s $'\t'

# Deep snapshot of the cheapest ASIN (product fields live under .data).
ASIN=$(echo "$SEARCH" | jq -r '
  .data.products
  | map(select((.is_sponsored | not) and (.price != null)))
  | sort_by(.price) | .[0].asin')

echo; echo "Snapshot for ASIN ${ASIN}:" >&2
# `price` is the buy-box price; `sold_by` / `has_buy_box` / `availability`
# replaced the old buybox[] array. For every competing seller on the ASIN,
# call /api/v1/amazon/offers instead.
curl -sS -X POST "${API}/amazon/product" -H "$AUTH" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg a "$ASIN" '{query:$a}')" \
| jq '{
    asin: .data.asin, title: .data.title, brand: .data.brand,
    price: .data.price, list_price: .data.list_price, currency: .data.currency,
    rating: .data.rating, reviews_count: .data.reviews_count,
    availability: .data.availability,
    seller: .data.sold_by, has_buy_box: .data.has_buy_box,
    other_sellers_count: .data.other_sellers_count,
    credits_used, credits_remaining
  }'
