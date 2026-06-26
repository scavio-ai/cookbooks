# Jupyter notebooks

Self-contained tutorial notebooks built on [`langchain-scavio`](https://pypi.org/project/langchain-scavio/)
and the [Scavio API](https://scavio.dev). Each is under ~15 cells with
pre-populated output -- open, run, adapt.

> **Get a free Scavio API key (50 free credits, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
pip install -r ../requirements.txt jupyter
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
jupyter notebook seo-keyword-researcher.ipynb
```

## Notebooks

### Google / SEO
- **`seo-keyword-researcher.ipynb`** -- PAA + related-search keyword research. Powered by the [Scavio Google SERP API](https://scavio.dev) -- a free [Ahrefs alternative](https://dashboard.scavio.dev).
- **`content-gap-finder.ipynb`** -- find content gaps competitors missed. Built on the [Scavio Google Search API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`news-aggregator.ipynb`** -- real-time news briefing. Uses the [Scavio Google News API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`google-knowledge-graph-extractor.ipynb`** -- structured entity facts. Taps the [Scavio Knowledge Graph API](https://scavio.dev) -- [free credits](https://dashboard.scavio.dev).

### Amazon / Walmart
- **`amazon-price-tracker.ipynb`** -- competitor price monitoring. Powered by the [Scavio Amazon API](https://scavio.dev) -- a free [Keepa alternative](https://dashboard.scavio.dev).
- **`amazon-bestseller-rank-tracker.ipynb`** -- category leaders and why they win. Built on the [Scavio Amazon API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`walmart-deal-finder.ipynb`** -- rank deals in any Walmart category. Uses the [Scavio Walmart API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`retail-arbitrage-finder.ipynb`** -- Walmart-to-Amazon resale finder. Built with the [Scavio retail APIs](https://scavio.dev) -- a free [Tactical Arbitrage alternative](https://dashboard.scavio.dev).
- **`multiplatform-product-comparison.ipynb`** -- side-by-side across stores. Powered by the [Scavio search API](https://scavio.dev) -- [free 50 credits](https://dashboard.scavio.dev).
- **`fake-review-detector.ipynb`** -- cross-reference Amazon vs YouTube reviewers. Built on the [Scavio Amazon + YouTube APIs](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).

### YouTube
- **`youtube-trend-tracker.ipynb`** -- trending videos and rising creators. Powered by the [Scavio YouTube API](https://scavio.dev) -- a free [VidIQ alternative](https://dashboard.scavio.dev).
- **`youtube-transcript-summarizer.ipynb`** -- analyze video engagement and content. Uses the [Scavio YouTube API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`youtube-to-blog-post.ipynb`** -- turn videos into SEO blog outlines. Built on the [Scavio YouTube API](https://scavio.dev) -- [free credits](https://dashboard.scavio.dev).

### Reddit
- **`reddit-sentiment-analyzer.ipynb`** -- classify brand/product sentiment. Powered by the [Scavio Reddit Search API](https://scavio.dev) -- a free [Brand24 alternative](https://dashboard.scavio.dev).
- **`reddit-market-research.ipynb`** -- mine recommendation threads. Built on the [Scavio Reddit API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).

### TikTok / Instagram
- **`tiktok-hashtag-analyzer.ipynb`** -- hashtag performance and top videos. Powered by the [Scavio TikTok API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`tiktok-comment-sentiment.ipynb`** -- audience sentiment from comments. Uses the [Scavio TikTok API](https://scavio.dev) -- [free credits](https://dashboard.scavio.dev).
- **`instagram-hashtag-analyzer.ipynb`** -- rank Instagram hashtags by volume. Built with the [Scavio Instagram API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`instagram-profile-analytics.ipynb`** -- engagement rate + content themes. Powered by the [Scavio Instagram API](https://scavio.dev) -- a free [HypeAuditor alternative](https://dashboard.scavio.dev).

---

Build real-time search into your own notebooks and agents with **[Scavio](https://scavio.dev)** -- [read the docs](https://scavio.dev/docs).
