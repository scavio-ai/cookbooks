# Raw REST recipes (curl + jq)

No SDK, no LLM -- just `curl` against the Scavio API and `jq` to reshape the
JSON. The shortest path to seeing the API work, and easy to port to any
language or drop in cron.

## Setup

```bash
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
# requires: curl, jq  (brew install jq)
```

All endpoints are `POST https://api.scavio.dev/api/v1/...` with
`Authorization: Bearer $SCAVIO_API_KEY`.

## Recipes

| Script | What it does | Platform |
|---|---|---|
| `google-serp-to-json.sh` | SERP -> compact JSON (organic, PAA, related) | Google |
| `amazon-price-snapshot.sh` | Search -> top-ASIN price/rating/seller snapshot | Amazon |
| `reddit-keyword-firehose.sh` | Poll "new" for a keyword, dedupe seen ids (cron) | Reddit |
| `youtube-search-to-metadata.sh` | Search -> full metadata for the top video | YouTube |
| `instagram-profile-card.sh` | Public profile -> scouting card | Instagram |
| `tiktok-hashtag-to-csv.sh` | Hashtag -> CSV of top videos | TikTok |

## Wire-format quirks worth remembering

- YouTube search uses the `search` field (not `query`).
- Amazon product takes the ASIN in the `query` field.
- Walmart product takes `product_id`.
- Reddit and Instagram calls cost 2 credits; most others cost 1.
