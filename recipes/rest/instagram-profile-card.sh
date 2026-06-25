#!/usr/bin/env bash
#
# instagram-profile-card.sh -- Instagram profile to a clean text card.
#
# Pulls a public Instagram profile and prints a compact scouting card:
# followers, following, posts, verified status, category, and bio. The
# building block for influencer vetting and competitor tracking.
#
# Requires: curl, jq, SCAVIO_API_KEY (https://dashboard.scavio.dev).
# Instagram endpoints cost 2 credits per call.
#
# Usage:
#   ./instagram-profile-card.sh nike
#
set -euo pipefail

: "${SCAVIO_API_KEY:?Set SCAVIO_API_KEY (https://dashboard.scavio.dev)}"
USERNAME="${1:-nike}"

curl -sS -X POST https://api.scavio.dev/api/v1/instagram/profile \
  -H "Authorization: Bearer ${SCAVIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg u "$USERNAME" '{username:$u}')" \
| jq -r '.data | "
  @\(.username)\(if .is_verified then "  [verified]" else "" end)
  \(.full_name // "")
  ----------------------------------------
  Followers:  \(.follower_count)
  Following:  \(.following_count)
  Posts:      \(.media_count)
  Category:   \(.category // "n/a")
  Private:    \(.is_private)
  Website:    \(.external_url // "n/a")
  ----------------------------------------
  \(.biography // "")
"'
