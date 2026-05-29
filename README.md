# Scavio Cookbook: LangChain Agents & Jupyter Notebooks for Amazon, Google, YouTube, Walmart, Reddit & TikTok

**22 production-ready AI agents and notebooks** that search Amazon products, Google results, YouTube videos, Walmart listings, Reddit threads, and TikTok creators in real time -- built with [LangChain](https://github.com/langchain-ai/langchain) and powered by the [Scavio](https://scavio.dev) search API.

[![PyPI](https://img.shields.io/pypi/v/langchain-scavio.svg?label=langchain-scavio)](https://pypi.org/project/langchain-scavio/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Scavio](https://img.shields.io/badge/powered%20by-Scavio-ff4d00.svg)](https://scavio.dev)

> **250 free API credits every month. No credit card required.** [Get your free key in 30 seconds](https://dashboard.scavio.dev)

---

## What's inside

- **22 working examples** -- 8 Python agents + 14 Jupyter notebooks you can run in under 5 minutes
- **Real search APIs** -- not scrapers, not mocks -- Amazon, Google, YouTube, Walmart, Reddit, TikTok
- **LangChain `create_agent` examples** with tool calling, multi-step reasoning, and grounded outputs
- **Free alternative** to SerpAPI, ScraperAPI, Bright Data, Jungle Scout, Fakespot, GummySearch, Modash, and $149/month SEO tools

## Quick Start (5 minutes)

### Run an agent

```bash
git clone https://github.com/scavio-ai/cookbooks.git
cd cookbooks

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env with SCAVIO_API_KEY (free) and OPENAI_API_KEY

python agents/amazon-agent.py "best wired earbuds under $50"
```

### Run a notebook

```bash
pip install jupyter
jupyter notebook notebooks/seo-keyword-researcher.ipynb
```

## Cookbook Catalog

### Amazon

| Cookbook | Type | Description |
|---------|------|-------------|
| [AmazonScout](agents/amazon-agent.py) | Agent | Product research with grounded recommendations |
| [ShoppingAssistant](agents/shopping-agent.py) | Agent | Conversational shopping assistant with comparisons |
| [Amazon Price Tracker](notebooks/amazon-price-tracker.ipynb) | Notebook | Competitor price monitoring across products |

### Walmart

| Cookbook | Type | Description |
|---------|------|-------------|
| [Walmart Deal Finder](notebooks/walmart-deal-finder.ipynb) | Notebook | Find and rank deals in any Walmart category |

### Google / SEO

| Cookbook | Type | Description |
|---------|------|-------------|
| [SEO Keyword Researcher](notebooks/seo-keyword-researcher.ipynb) | Notebook | Extract PAA questions and related searches for keyword clustering |
| [Content Gap Finder](notebooks/content-gap-finder.ipynb) | Notebook | Find content gaps your competitors missed |
| [News Aggregator](notebooks/news-aggregator.ipynb) | Notebook | Real-time news briefing from Google search |

### YouTube

| Cookbook | Type | Description |
|---------|------|-------------|
| [TrendTap](agents/trendtap.py) | Agent | YouTube + Reddit content gap finder for creators |
| [YouTube Trend Tracker](notebooks/youtube-trend-tracker.ipynb) | Notebook | Track trending videos and rising creators in any niche |
| [YouTube Video Research](notebooks/youtube-transcript-summarizer.ipynb) | Notebook | Analyze video engagement, metadata, and content trends |
| [YouTube to Blog Post](notebooks/youtube-to-blog-post.ipynb) | Notebook | Convert YouTube videos into SEO-optimized blog outlines |

### Reddit

| Cookbook | Type | Description |
|---------|------|-------------|
| [RedditRadar](agents/reddit-radar.py) | Agent | Find live Reddit threads for soft-promo and GTM |
| [BrandPulse](agents/brandpulse.py) | Agent | Reddit + Google brand sentiment monitor |
| [Reddit Sentiment Analyzer](notebooks/reddit-sentiment-analyzer.ipynb) | Notebook | Classify brand/product sentiment from Reddit discussions |
| [Reddit Market Research](notebooks/reddit-market-research.ipynb) | Notebook | Mine recommendation threads for product insights |

### TikTok

| Cookbook | Type | Description |
|---------|------|-------------|
| [TikFluencer](agents/tikfluencer.py) | Agent | TikTok influencer discovery for product campaigns |
| [TikTok Hashtag Analyzer](notebooks/tiktok-hashtag-analyzer.ipynb) | Notebook | Analyze hashtag performance, top videos, and comment sentiment |

### Multi-Platform

| Cookbook | Type | Description |
|---------|------|-------------|
| [PriceWar](agents/pricewar.py) | Agent | Amazon vs Walmart arbitrage finder for resellers |
| [BuyOrNot](agents/buyornot.py) | Agent | Multi-platform buy/skip verdict across 5 sources |
| [Multi-Platform Comparison](notebooks/multiplatform-product-comparison.ipynb) | Notebook | Side-by-side product comparison across Amazon, Walmart, and Google |
| [Fake Review Detector](notebooks/fake-review-detector.ipynb) | Notebook | Cross-reference Amazon ratings with YouTube reviewer signals |
| [Retail Arbitrage Finder](notebooks/retail-arbitrage-finder.ipynb) | Notebook | Find Walmart products to resell on Amazon for profit |

All agents are **single-file, under 200 lines, MIT licensed**. All notebooks are **self-contained tutorials with pre-populated output**. Fork, adapt, ship.

## Why Scavio vs. the alternatives

| Need | Expensive tool | Scavio + LangChain |
|------|----------------|---------------------|
| Amazon product search API | Jungle Scout ($49-129/mo) | Free (250 calls/mo) |
| SERP + People Also Ask | SerpAPI ($75/mo) | Free (250 calls/mo) |
| YouTube video metadata | VidIQ/TubeBuddy ($7-49/mo) | One API call |
| Fake review detection | Fakespot Premium | Cross-reference YouTube reviews for free |
| Brand monitoring | Brand24 ($99-299/mo) | Free with BrandPulse agent |
| SEO content gap analysis | Ahrefs ($99-449/mo) | Free with Content Gap Finder notebook |
| Reddit lead / GTM tracking | GummySearch ($29-99/mo) | Free with RedditRadar agent |
| TikTok influencer discovery | Modash ($99-399/mo) | Free with TikFluencer agent |
| Retail arbitrage tools | Tactical Arbitrage ($59-99/mo) | Free with Retail Arbitrage notebook |

## LangChain Tools Reference

Install once -- every agent and notebook uses the same tools via [langchain-scavio](https://pypi.org/project/langchain-scavio/):

```python
from langchain_scavio import (
    ScavioSearch,              # Google search: results, news, PAA, knowledge graph
    ScavioAmazonSearch,        # Amazon product search
    ScavioAmazonProduct,       # Amazon product details by ASIN
    ScavioWalmartSearch,       # Walmart product search
    ScavioWalmartProduct,      # Walmart product details
    ScavioYouTubeSearch,       # YouTube video, channel, playlist search
    ScavioYouTubeMetadata,     # YouTube video metadata (views, likes, tags)
    ScavioRedditSearch,        # Reddit post and comment search
    ScavioRedditPost,          # Reddit post body and comment thread
    ScavioTikTokProfile,       # TikTok user profile lookup
    ScavioTikTokUserPosts,     # TikTok user's posted videos
    ScavioTikTokSearchUsers,   # TikTok user search by keyword
    ScavioTikTokHashtag,       # TikTok hashtag info and ID lookup
    ScavioTikTokHashtagVideos, # TikTok videos by hashtag
    ScavioTikTokVideoComments, # TikTok video comments
)
```

## Build Your Own Agent in 30 Lines

```python
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioAmazonSearch, ScavioAmazonProduct

load_dotenv(override=True)

agent = create_agent(
    ChatOpenAI(model="gpt-4o", temperature=0),
    tools=[ScavioAmazonSearch(max_results=5), ScavioAmazonProduct()],
    system_prompt="You are a shopping research agent. Cite ASINs.",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "best wired earbuds under $50"}]
})
print(result["messages"][-1].content)
```

Full reference implementation: [agents/amazon-agent.py](agents/amazon-agent.py)

## FAQ

**Is this a free alternative to SerpAPI or ScraperAPI?**
Yes. Scavio gives you 250 free real-time search credits per month across Google, Amazon, YouTube, Walmart, Reddit, and TikTok -- enough to build and ship most personal projects or MVPs.

**Does it work with OpenAI GPT-4o, Claude, and other LLMs?**
Yes. Every agent uses LangChain's `create_agent`, so you can swap in any chat model: OpenAI, Anthropic Claude, Google Gemini, Groq, local Ollama models, etc.

**Can I use this for e-commerce price monitoring or dropshipping research?**
Yes. The Amazon + Walmart tools return live pricing, stock, ratings, ASINs, and reviews. See the [Amazon Price Tracker](notebooks/amazon-price-tracker.ipynb), [Retail Arbitrage Finder](notebooks/retail-arbitrage-finder.ipynb), and [PriceWar](agents/pricewar.py) agents for examples.

**How do I get YouTube video metadata?**
Use `ScavioYouTubeSearch` to find videos and `ScavioYouTubeMetadata` to get full details (views, likes, tags, description) for any public YouTube video.

**Is scraping Amazon legal?**
Scavio is a licensed real-time search provider -- you call Scavio's API, not Amazon's. Your agent stays compliant and your IP never gets blocked.

**Can I use this for Reddit marketing or GTM?**
Yes. `ScavioRedditSearch` and `ScavioRedditPost` let you find live threads where your audience is asking for what you built. The [RedditRadar](agents/reddit-radar.py) agent ranks those threads by engagement potential -- recency, subreddit fit, whether the ask is still open -- so you can spend time engaging instead of hunting. Free alternative to GummySearch and F5Bot.

**Can I find TikTok influencers with this?**
Yes. The [TikFluencer](agents/tikfluencer.py) agent searches TikTok creators by keyword and hashtag, profiles them, analyzes content fit and engagement quality, and returns a ranked shortlist. Free alternative to Modash, Heepsy, and Upfluence.

## Contributing

PRs welcome. Guidelines:

- One agent per file, under 200 lines
- One notebook per topic, under 15 cells
- Short docstring with prerequisites and usage
- Verified against the free tier (250 credits/month)
- No emojis, no generated-by-AI attribution

## Resources

- [Scavio Dashboard](https://dashboard.scavio.dev) -- free API key
- [Scavio Docs](https://scavio.dev/docs) -- REST + MCP reference
- [langchain-scavio on PyPI](https://pypi.org/project/langchain-scavio/)
- [LangChain Agents Guide](https://docs.langchain.com/oss/python/langchain/agents)

---

**Keywords:** langchain amazon api, amazon product search api python, free serpapi alternative, ai shopping agent, langchain agent examples, amazon scraper api free, walmart api langchain, ai agent cookbook, openai amazon agent, gpt-4 shopping assistant, langchain tool calling examples, free amazon product api, ai price comparison agent, fake review detector open source, ai seo content gap finder, brand monitoring open source, retail arbitrage tool open source, people also ask api, google serp api free, langchain reddit api, reddit search api python, free gummysearch alternative, reddit lead generation tool, reddit gtm agent, tiktok influencer finder, tiktok api langchain, tiktok creator search api, influencer discovery agent, tiktok marketing tool open source, free tiktok analytics api, jupyter notebook amazon api, youtube video analysis python, reddit sentiment analysis notebook, seo keyword research notebook, tiktok hashtag analytics python, walmart deals finder notebook, free keepa alternative, free camelcamelcamel alternative, content gap analysis python, youtube to blog post python, retail arbitrage finder python, multi platform product comparison, amazon vs walmart price comparison python.

Powered by **[Scavio](https://scavio.dev)** -- the real-time search API for AI agents.
