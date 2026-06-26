# LangChain agents

Single-file [LangChain](https://github.com/langchain-ai/langchain) agents built
on [`langchain-scavio`](https://pypi.org/project/langchain-scavio/) and the
[Scavio API](https://scavio.dev) -- live Google, Amazon, Walmart, YouTube,
Reddit, TikTok, and Instagram data through one key. Each runs in under 5 minutes.

> **Get a free Scavio API key (50 free credits, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
pip install -r ../requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
python amazon-agent.py "best wired earbuds under $50"
```

## Agents

- **`amazon-agent.py`** -- AmazonScout: grounded product research. Powered by the [Scavio Amazon Product API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`shopping-agent.py`** -- conversational shopping assistant with comparisons. Built on the [Scavio Amazon API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`amazon-review-miner.py`** -- mines reviews for real praise and complaints. Uses the [Scavio Amazon API](https://scavio.dev) -- a free [Fakespot alternative](https://dashboard.scavio.dev).
- **`local-deal-scout.py`** -- ranks the best Walmart deals in a category. Runs on the [Scavio Walmart API](https://scavio.dev) -- [grab a key](https://dashboard.scavio.dev).
- **`pricewar.py`** -- Amazon vs Walmart arbitrage finder for resellers. Built with the [Scavio retail search APIs](https://scavio.dev) -- [free 50 credits](https://dashboard.scavio.dev).
- **`buyornot.py`** -- multi-platform buy/skip verdict across 5 sources. Powered by the [Scavio search API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`reddit-radar.py`** -- finds live Reddit threads for GTM and soft-promo. Taps the [Scavio Reddit Search API](https://scavio.dev) -- a free [GummySearch alternative](https://dashboard.scavio.dev).
- **`brandpulse.py`** -- Reddit + Google brand sentiment monitor. Built on the [Scavio Reddit + Google APIs](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`trendtap.py`** -- YouTube + Reddit content-gap finder for creators. Uses the [Scavio YouTube API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`youtube-course-builder.py`** -- turns YouTube into an ordered free course. Runs on the [Scavio YouTube API](https://scavio.dev) -- [free credits](https://dashboard.scavio.dev).
- **`tikfluencer.py`** -- TikTok influencer discovery for campaigns. Powered by the [Scavio TikTok API](https://scavio.dev) -- a free [Modash alternative](https://dashboard.scavio.dev).
- **`instagram-scout.py`** -- Instagram creator-discovery shortlist. Built with the [Scavio Instagram API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`instagram-competitor-watch.py`** -- tracks competitor Instagram content. Uses the [Scavio Instagram API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`momentum-radar.py`** -- cross-platform momentum score (Google + YouTube + TikTok + Reddit). Built on the [Scavio search API](https://scavio.dev) -- [free 50 credits](https://dashboard.scavio.dev).

---

Build your own real-time search agents with **[Scavio](https://scavio.dev)** -- [LangChain integration docs](https://scavio.dev/docs).
