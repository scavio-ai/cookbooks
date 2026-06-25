#!/usr/bin/env bash
#
# amazon-price-snapshot.sh -- Amazon search to a price snapshot table.
#
# Searches Amazon for a keyword, then pulls full product detail for the top
# ASIN (price, rating, buybox seller, stock) -- the two-call pattern every
# price tracker or arbitrage tool is built on. A free alternative to Keepa
# and Jungle Scout for ad-hoc checks.
#
# Note the wire quirk: the product endpoint takes the ASIN in the "query"
# field, not an "asin" field.
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

# Top 5 organic results, deduped by ASIN and ordered by organic position.
SEARCH=$(curl -sS -X POST "${API}/amazon/search" -H "$AUTH" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg q "$QUERY" '{query:$q}')")

echo "$SEARCH" | jq -r '
  .data.products
  | map(select(.is_sponsored | not))
  | unique_by(.asin) | sort_by(.organic_position // 999) | .[:5][]
  | [.asin, (.price // "n/a"), (.rating // "n/a"), (.reviews_count // 0), .title] | @tsv' \
| column -t -s $'\t'

# Deep snapshot of the top organic ASIN (product fields live under .data).
ASIN=$(echo "$SEARCH" | jq -r '
  .data.products | map(select(.is_sponsored | not))
  | sort_by(.organic_position // 999) | .[0].asin')

echo; echo "Snapshot for top ASIN ${ASIN}:" >&2
curl -sS -X POST "${API}/amazon/product" -H "$AUTH" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg a "$ASIN" '{query:$a}')" \
| jq '{
    asin: .data.asin, title: .data.title, brand: .data.brand,
    price: (.data.buybox[0].price // .data.price),
    rating: .data.rating, reviews_count: .data.reviews_count,
    in_stock: (.data.buybox[0].stock // null),
    seller: (.data.buybox[0].seller_name // null),
    credits_used, credits_remaining
  }'
