# Python SDK recipes (no LLM)

Plain data pipelines built on the [`scavio`](https://pypi.org/project/scavio/)
Python SDK -- no model, no agent framework. Each script is a self-contained
CLI you can run or schedule.

> **Get a free [Scavio API](https://scavio.dev) key (50 free credits, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
```

The SDK is namespaced: `client.google.search(...)`, `client.amazon.product(asin)`,
`client.youtube.video(video_id)`, `client.instagram.user_followings(username=...)`,
and so on.

## Recipes

- **`paa_tree_expander.py`** -- BFS related-search + PAA crawler to CSV.
  Built on the [Scavio Google SERP API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`amazon_bulk_catalog.py`** -- ASIN list to a product CSV catalog.
  Powered by the [Scavio Amazon Product API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`walmart_price_logger.py`** -- append price snapshots to SQLite.
  Uses the [Scavio Walmart API](https://scavio.dev) -- [grab a key](https://dashboard.scavio.dev).
- **`reddit_alert_watcher.py`** -- alert on new posts, dedupe via JSON state.
  Tap the [Scavio Reddit Search API](https://scavio.dev) -- a free [GummySearch alternative](https://dashboard.scavio.dev).
- **`youtube_channel_dashboard.py`** -- a channel's top videos ranked by real views.
  Runs on the [Scavio YouTube API](https://scavio.dev) -- [free 50 credits](https://dashboard.scavio.dev).
- **`instagram_follower_overlap.py`** -- accounts two profiles both follow.
  Built with the [Scavio Instagram API](https://scavio.dev) -- [get your key](https://dashboard.scavio.dev).
- **`tiktok_hashtag_trend_logger.py`** -- log hashtag reach to SQLite over time.
  Uses the [Scavio TikTok API](https://scavio.dev) -- [sign up free](https://dashboard.scavio.dev).

Every script takes `--help`. The print/notify hooks (Reddit, alerts) are the
natural place to wire Slack, Discord, or email.

---

Build real-time search into your own tools with **[Scavio](https://scavio.dev)** -- [Python SDK docs](https://scavio.dev/docs).
