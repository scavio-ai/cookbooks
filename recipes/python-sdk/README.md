# Python SDK recipes (no LLM)

Plain data pipelines built on the [`scavio`](https://pypi.org/project/scavio/)
Python SDK -- no model, no agent framework. Each script is a self-contained
CLI you can run or schedule.

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
```

The SDK is namespaced: `client.google.search(...)`, `client.amazon.product(asin)`,
`client.youtube.metadata(video_id)`, `client.instagram.user_followings(username=...)`,
and so on.

## Recipes

| Script | What it does | Platform |
|---|---|---|
| `paa_tree_expander.py` | BFS related-search + PAA crawler -> CSV | Google |
| `amazon_bulk_catalog.py` | ASIN list -> product CSV catalog | Amazon |
| `walmart_price_logger.py` | Append price snapshots to SQLite | Walmart |
| `reddit_alert_watcher.py` | Alert on new posts, dedupe via JSON state | Reddit |
| `youtube_channel_dashboard.py` | Top videos ranked by real engagement | YouTube |
| `instagram_follower_overlap.py` | Accounts two profiles both follow | Instagram |
| `tiktok_hashtag_trend_logger.py` | Log hashtag reach to SQLite over time | TikTok |

Every script takes `--help`. The print/notify hooks (Reddit, alerts) are the
natural place to wire Slack, Discord, or email.
