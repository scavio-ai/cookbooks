#!/usr/bin/env bash
#
# youtube-search-to-metadata.sh -- search YouTube, then enrich with metadata.
#
# Searches YouTube for a query, takes the top video, and pulls full metadata
# (views, likes, comments, duration, channel, upload date) -- the search ID
# feeds straight into the metadata call. A free alternative to VidIQ for
# spot research.
#
# Wire quirk: the YouTube search endpoint takes the term in the "search"
# field, not "query".
#
# Requires: curl, jq, SCAVIO_API_KEY (https://dashboard.scavio.dev).
#
# Usage:
#   ./youtube-search-to-metadata.sh "python async tutorial"
#
set -euo pipefail

: "${SCAVIO_API_KEY:?Set SCAVIO_API_KEY (https://dashboard.scavio.dev)}"
QUERY="${*:-python async tutorial}"
API="https://api.scavio.dev/api/v1"
AUTH="Authorization: Bearer ${SCAVIO_API_KEY}"

VIDEO_ID=$(curl -sS -X POST "${API}/youtube/search" -H "$AUTH" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg s "$QUERY" '{search:$s, sort_by:"view_count"}')" \
  | jq -r '.data.results[0].videoId')

echo "Top video for \"${QUERY}\": ${VIDEO_ID}" >&2

curl -sS -X POST "${API}/youtube/metadata" -H "$AUTH" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg v "$VIDEO_ID" '{video_id:$v}')" \
| jq '.data | {
    video_id, title, uploader, channel_url,
    view_count, like_count, comment_count,
    duration_seconds: .duration, upload_date,
    url: ("https://youtube.com/watch?v=" + .video_id)
  }'
