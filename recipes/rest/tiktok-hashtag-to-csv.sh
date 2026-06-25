#!/usr/bin/env bash
#
# tiktok-hashtag-to-csv.sh -- TikTok hashtag to a CSV of top videos.
#
# Resolves a hashtag name to its TikTok ID, pulls the videos posted under
# it, and writes a CSV (video id, author, plays, likes, comments, shares,
# caption). Feed it into a spreadsheet for trend or campaign research.
#
# Two-call pattern: hashtag(name) -> challengeInfo.challenge.id ->
# hashtag/videos(id).
#
# Requires: curl, jq, SCAVIO_API_KEY (https://dashboard.scavio.dev).
#
# Usage:
#   ./tiktok-hashtag-to-csv.sh coffee > coffee.csv
#
set -euo pipefail

: "${SCAVIO_API_KEY:?Set SCAVIO_API_KEY (https://dashboard.scavio.dev)}"
HASHTAG="${1:-coffee}"
API="https://api.scavio.dev/api/v1"
AUTH="Authorization: Bearer ${SCAVIO_API_KEY}"

HASHTAG_ID=$(curl -sS -X POST "${API}/tiktok/hashtag" -H "$AUTH" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg h "$HASHTAG" '{hashtag_name:$h}')" \
  | jq -r '.data.challengeInfo.challenge.id')

echo "Hashtag #${HASHTAG} resolved to id ${HASHTAG_ID}" >&2

echo "video_id,author,plays,likes,comments,shares,caption"
curl -sS -X POST "${API}/tiktok/hashtag/videos" -H "$AUTH" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg id "$HASHTAG_ID" '{hashtag_id:$id, count:30}')" \
| jq -r '.data.aweme_list[]? | [
    .aweme_id,
    (.author.unique_id // .author.nickname // ""),
    (.statistics.play_count // 0),
    (.statistics.digg_count // 0),
    (.statistics.comment_count // 0),
    (.statistics.share_count // 0),
    ((.desc // "") | gsub("[\r\n,]"; " "))
  ] | @csv'
