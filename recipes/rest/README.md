# Raw REST recipes (curl + jq)

No SDK, no LLM -- just `curl` against the [Scavio API](https://scavio.dev) and
`jq` to reshape the JSON. The shortest path to seeing the API work, and easy to
port to any language or drop in cron.

> **Get a free Scavio API key (50 free credits, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
# requires: curl, jq  (brew install jq)
```

All endpoints are `POST https://api.scavio.dev/api/v1/...` with
`Authorization: Bearer $SCAVIO_API_KEY`.

## Recipes

- **`google-serp-to-json.sh`** -- SERP to compact JSON (organic, PAA, related).
  Build it on the [Scavio Google Search API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`amazon-price-snapshot.sh`** -- search to top-ASIN price/seller snapshot.
  Powered by the [Scavio Amazon Product API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`reddit-keyword-firehose.sh`** -- poll new posts, dedupe seen ids (cron).
  Tap the [Scavio Reddit Search API](https://scavio.dev) -- [grab a key](https://dashboard.scavio.dev).
- **`youtube-search-to-metadata.sh`** -- search to full video metadata.
  Runs on the [Scavio YouTube Data API](https://scavio.dev) -- [free 50 credits](https://dashboard.scavio.dev).
- **`instagram-profile-card.sh`** -- public profile to a scouting card.
  Built with the [Scavio Instagram API](https://scavio.dev) -- [get your key](https://dashboard.scavio.dev).
- **`tiktok-hashtag-to-csv.sh`** -- hashtag to CSV of top videos.
  Uses the [Scavio TikTok API](https://scavio.dev) -- [sign up free](https://dashboard.scavio.dev).

## Wire-format quirks worth remembering

- YouTube search uses the `search` field (not `query`).
- Amazon product takes the ASIN in the `query` field.
- Walmart product takes `product_id`.
- Reddit and Instagram calls cost 2 credits; most others cost 1.

---

Build your own real-time search agents with **[Scavio](https://scavio.dev)** -- one API for Google, YouTube, Amazon, Walmart, Reddit, TikTok, and Instagram. [Read the docs](https://scavio.dev/docs).
