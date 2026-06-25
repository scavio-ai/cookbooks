# Pure API scrapers (one per endpoint)

Single-file Python scrapers that hit a [Scavio API](https://scavio.dev)
endpoint directly with `requests` and print the raw JSON. No SDK, no framework,
no LLM, no use case -- just scrape and return the data. One script per endpoint
across all seven platforms.

> **Get a free Scavio API key (250 credits/month, no credit card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev

python google_search_scraper.py "coffee makers"
python tiktok_comment_scraper.py "7653149441393708320" | jq .
```

Every script: `POST https://api.scavio.dev/api/v1/<endpoint>` with
`Authorization: Bearer $SCAVIO_API_KEY`, prints indented JSON to stdout.

## Scrapers

### Google
- **`google_search_scraper.py`** -- Google SERP (organic, PAA, related, knowledge graph). [Scavio Google Search API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).

### YouTube
- **`youtube_search_scraper.py`** -- YouTube search results. [Scavio YouTube API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`youtube_video_scraper.py`** -- full video metadata by id. [Scavio YouTube API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).

### Amazon
- **`amazon_search_scraper.py`** -- Amazon product search. [Scavio Amazon API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`amazon_product_scraper.py`** -- full product detail by ASIN. [Scavio Amazon Product API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).

### Walmart
- **`walmart_search_scraper.py`** -- Walmart product search. [Scavio Walmart API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`walmart_product_scraper.py`** -- full product detail by id. [Scavio Walmart API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).

### Reddit
- **`reddit_search_scraper.py`** -- Reddit post search. [Scavio Reddit API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`reddit_post_scraper.py`** -- post body + comment thread by URL. [Scavio Reddit API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).

### TikTok
- **`tiktok_profile_scraper.py`** -- user profile by username. [Scavio TikTok API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`tiktok_user_posts_scraper.py`** -- a user's videos by sec_user_id. [Scavio TikTok API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`tiktok_video_scraper.py`** -- single video detail by id. [Scavio TikTok API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`tiktok_comment_scraper.py`** -- comments on a video. [Scavio TikTok API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`tiktok_comment_replies_scraper.py`** -- replies to a comment. [Scavio TikTok API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`tiktok_video_search_scraper.py`** -- videos by keyword. [Scavio TikTok API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`tiktok_user_search_scraper.py`** -- creators by keyword. [Scavio TikTok API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`tiktok_hashtag_scraper.py`** -- hashtag info + id by name. [Scavio TikTok API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`tiktok_hashtag_videos_scraper.py`** -- videos under a hashtag id. [Scavio TikTok API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`tiktok_followers_scraper.py`** -- a user's followers. [Scavio TikTok API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`tiktok_followings_scraper.py`** -- accounts a user follows. [Scavio TikTok API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).

### Instagram
- **`instagram_profile_scraper.py`** -- profile by username. [Scavio Instagram API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`instagram_user_posts_scraper.py`** -- recent posts. [Scavio Instagram API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`instagram_reels_scraper.py`** -- a user's reels. [Scavio Instagram API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`instagram_tagged_scraper.py`** -- posts a user is tagged in. [Scavio Instagram API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`instagram_stories_scraper.py`** -- active stories. [Scavio Instagram API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`instagram_post_scraper.py`** -- single post by shortcode. [Scavio Instagram API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`instagram_comment_scraper.py`** -- comments on a post. [Scavio Instagram API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`instagram_comment_replies_scraper.py`** -- replies to a comment. [Scavio Instagram API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`instagram_user_search_scraper.py`** -- users by keyword. [Scavio Instagram API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`instagram_hashtag_search_scraper.py`** -- hashtags by keyword. [Scavio Instagram API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).
- **`instagram_followers_scraper.py`** -- a user's followers. [Scavio Instagram API](https://scavio.dev) - [free key](https://dashboard.scavio.dev).
- **`instagram_followings_scraper.py`** -- accounts a user follows. [Scavio Instagram API](https://scavio.dev) - [start free](https://dashboard.scavio.dev).

## Wire-format quirks (handled for you)

- YouTube search takes the term in the `search` field (not `query`).
- Amazon product takes the ASIN in the `query` field.
- Walmart product takes `product_id`; TikTok user endpoints take `sec_user_id`
  (get it from `tiktok_profile_scraper.py`).
- Reddit and Instagram calls cost 2 credits; most others cost 1.

---

Scrape Google, YouTube, Amazon, Walmart, Reddit, TikTok, and Instagram from one API with **[Scavio](https://scavio.dev)** -- [get a free key](https://dashboard.scavio.dev) | [read the docs](https://scavio.dev/docs).
