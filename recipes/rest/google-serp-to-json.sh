#!/usr/bin/env bash
#
# google-serp-to-json.sh -- Google SERP to clean JSON with curl + jq.
#
# Pulls organic results, People Also Ask, and related searches from the
# Scavio Google endpoint and reshapes the raw response into a compact JSON
# object you can pipe into anything. A free alternative to SerpAPI.
#
# Requires: curl, jq, and a free Scavio API key (https://dashboard.scavio.dev).
#   export SCAVIO_API_KEY="sk_..."
#
# Usage:
#   ./google-serp-to-json.sh "best running shoes 2026"
#   ./google-serp-to-json.sh "best running shoes 2026" > serp.json
#
set -euo pipefail

: "${SCAVIO_API_KEY:?Set SCAVIO_API_KEY (https://dashboard.scavio.dev)}"
QUERY="${*:-best running shoes 2026}"

curl -sS -X POST https://api.scavio.dev/api/v1/google \
  -H "Authorization: Bearer ${SCAVIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg q "$QUERY" '{query:$q}')" \
| jq '{
    query: .query,
    organic: [.results[]? | {position, title, url, snippet: .content, domain}],
    people_also_ask: [.questions[]? | (.question // .)],
    related_searches: [.related_searches[]? | .query],
    credits_used, credits_remaining
  }'
