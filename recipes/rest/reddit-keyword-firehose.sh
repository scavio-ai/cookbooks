#!/usr/bin/env bash
#
# reddit-keyword-firehose.sh -- new Reddit posts for a keyword, cron-ready.
#
# Polls Reddit "new" for a keyword and prints any post it has not seen
# before (deduped via a local seen-ids file). Drop it in cron to get a
# poor-man's brand monitor or lead tracker -- a free alternative to F5Bot
# and GummySearch.
#
# Requires: curl, jq, SCAVIO_API_KEY (https://dashboard.scavio.dev).
# Reddit search costs 2 credits per call.
#
# Usage:
#   ./reddit-keyword-firehose.sh "serpapi alternative"
#   # cron: every 15 min
#   */15 * * * * SCAVIO_API_KEY=sk_... /path/reddit-keyword-firehose.sh "serpapi alternative" >> /var/log/firehose.log
#
set -euo pipefail

: "${SCAVIO_API_KEY:?Set SCAVIO_API_KEY (https://dashboard.scavio.dev)}"
QUERY="${*:-serpapi alternative}"
SEEN_FILE="${SEEN_FILE:-/tmp/scavio_seen_$(echo "$QUERY" | tr -cs 'a-zA-Z0-9' '_').txt}"
touch "$SEEN_FILE"

curl -sS -X POST https://api.scavio.dev/api/v1/reddit/search \
  -H "Authorization: Bearer ${SCAVIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg q "$QUERY" '{query:$q, sort:"new"}')" \
| jq -r '.data.posts[]? | [.id, .subreddit, .author, .title, .url] | @tsv' \
| while IFS=$'\t' read -r id sub author title url; do
    if ! grep -qxF "$id" "$SEEN_FILE"; then
      echo "$id" >> "$SEEN_FILE"
      printf 'NEW  r/%s  by u/%s\n  %s\n  %s\n\n' "$sub" "$author" "$title" "$url"
    fi
  done

echo "Done. Tracking $(wc -l < "$SEEN_FILE" | tr -d ' ') seen posts in ${SEEN_FILE}." >&2
