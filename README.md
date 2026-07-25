# Scavio Cookbook: 104 real-world examples for the Scavio search API

**104 runnable examples** -- AI agents, notebooks, no-code workflows, and a pure
scraper for every endpoint -- that search **Google, YouTube, Amazon, Walmart,
Reddit, TikTok, and Instagram** in real time, powered by the
[Scavio](https://scavio.dev) search API.

Built across **every way you'd actually use the API**: raw REST, the Python and
JS/TS SDKs, plain `requests` scrapers, LangChain, the Vercel AI SDK, CrewAI,
Agno, smolagents, Haystack, AutoGen, n8n, and MCP.

[![PyPI](https://img.shields.io/pypi/v/scavio.svg?label=scavio)](https://pypi.org/project/scavio/)
[![npm](https://img.shields.io/npm/v/scavio.svg?label=scavio)](https://www.npmjs.com/package/scavio)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Scavio](https://img.shields.io/badge/powered%20by-Scavio-ff4d00.svg)](https://scavio.dev)

> **50 free API credits to start (one-time). No credit card required.** [Get your free key in 30 seconds](https://dashboard.scavio.dev)

---

## What's inside

- **One API, seven platforms** -- Google, YouTube, Amazon, Walmart, Reddit, TikTok, Instagram.
- **Eleven integration surfaces** -- pick the one that matches your stack.
- **Free alternative** to SerpAPI, ScraperAPI, Bright Data, Jungle Scout, Fakespot, GummySearch, Modash, Keepa, and $149/month SEO tools.

| Surface | Folder | Examples | Lang |
|---|---|---|---|
| Raw REST (curl + jq) | [`recipes/rest`](recipes/rest) | 6 | bash |
| Pure API scrapers (one per endpoint) | [`recipes/scrapers`](recipes/scrapers) | 32 | Python |
| Python SDK (no LLM) | [`recipes/python-sdk`](recipes/python-sdk) | 7 | Python |
| JS/TS SDK (no LLM) | [`recipes/js-sdk`](recipes/js-sdk) | 6 | TypeScript |
| Vercel AI SDK | [`recipes/vercel-ai`](recipes/vercel-ai) | 4 | TypeScript |
| LangChain agents | [`agents`](agents) | 14 | Python |
| LangChain notebooks | [`notebooks`](notebooks) | 19 | Jupyter |
| CrewAI | [`recipes/crewai`](recipes/crewai) | 4 | Python |
| Agno | [`recipes/agno`](recipes/agno) | 3 | Python |
| smolagents | [`recipes/smolagents`](recipes/smolagents) | 2 | Python |
| Haystack | [`recipes/haystack`](recipes/haystack) | 2 | Python |
| AutoGen | [`recipes/autogen`](recipes/autogen) | 2 | Python |
| n8n (no-code) | [`recipes/n8n`](recipes/n8n) | 2 | JSON |
| MCP | [`recipes/mcp`](recipes/mcp) | 1 | Python/JSON |

Each `recipes/` subfolder has its own README and its own `requirements.txt` /
`package.json` -- so the frameworks never fight over dependencies.

## Quick start

Pick the stack you already use. Every example reads `SCAVIO_API_KEY` from the
environment (free key: https://dashboard.scavio.dev).

```bash
# Raw API -- no install
export SCAVIO_API_KEY="sk_..."
curl -s -X POST https://api.scavio.dev/api/v2/google \
  -H "Authorization: Bearer $SCAVIO_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"best running shoes 2026"}' | jq .

# Python SDK
pip install scavio
python -c "from scavio import ScavioClient; print(ScavioClient().google.search('hello')['organic_results'][0]['title'])"

# JS/TS SDK
npm install scavio
node -e "import('scavio').then(async({Scavio})=>console.log((await new Scavio().google.search({query:'hello'})).results[0].title))"
```

Then run a full example:

```bash
git clone https://github.com/scavio-ai/cookbooks.git && cd cookbooks
cp .env.example .env   # add SCAVIO_API_KEY (free) and OPENAI_API_KEY

# a LangChain agent
pip install -r requirements.txt
python agents/instagram-scout.py "specialty coffee creators, 10k-250k followers"

# a no-LLM SDK pipeline
pip install -r recipes/python-sdk/requirements.txt
python recipes/python-sdk/youtube_channel_dashboard.py "langchain agents tutorial"
```

## Catalog

### Raw REST -- `recipes/rest` (curl + jq, no LLM)
| Example | Platform |
|---|---|
| `google-serp-to-json.sh` -- SERP to clean JSON (organic, PAA, related) | Google |
| `amazon-price-snapshot.sh` -- search to top-ASIN price/seller snapshot | Amazon |
| `reddit-keyword-firehose.sh` -- poll new posts, dedupe seen ids (cron) | Reddit |
| `youtube-search-to-metadata.sh` -- search to full video metadata | YouTube |
| `instagram-profile-card.sh` -- profile to scouting card | Instagram |
| `tiktok-hashtag-to-csv.sh` -- hashtag to CSV of top videos | TikTok |

### Python SDK -- `recipes/python-sdk` (no LLM)
| Example | Platform |
|---|---|
| `paa_tree_expander.py` -- BFS related-search + PAA crawler to CSV | Google |
| `amazon_bulk_catalog.py` -- ASIN list to product CSV | Amazon |
| `walmart_price_logger.py` -- price snapshots to SQLite | Walmart |
| `reddit_alert_watcher.py` -- alert on new posts (JSON state) | Reddit |
| `youtube_channel_dashboard.py` -- a channel's top videos ranked by views | YouTube |
| `instagram_follower_overlap.py` -- accounts two profiles both follow | Instagram |
| `tiktok_hashtag_trend_logger.py` -- log hashtag reach to SQLite | TikTok |

### JS/TS SDK -- `recipes/js-sdk` (no LLM)
| Example | Platform |
|---|---|
| `google-news-feed.ts` -- news search to JSON feed | Google |
| `amazon-price-drop-webhook.ts` -- lowest price to Discord/Slack | Amazon |
| `reddit-to-slack.ts` -- new threads to Slack Block Kit | Reddit |
| `youtube-playlist-builder.ts` -- search to ranked playlist | YouTube |
| `instagram-engagement-rate.ts` -- profile + posts to engagement rate | Instagram |
| `tiktok-creator-scorecard.ts` -- creator search to scorecard | TikTok |

### Vercel AI SDK -- `recipes/vercel-ai`
| Example | Tools |
|---|---|
| `research-stream.ts` -- streamed, cited research answer | Google |
| `reddit-sentiment-tool.ts` -- brand/product sentiment | Reddit |
| `instagram-influencer-vet.ts` -- creator discovery + vetting | Instagram |
| `shopping-route.ts` -- Next.js shopping endpoint | Amazon + Walmart |

### LangChain -- `agents` (new) + `notebooks` (new)
| New agent | Platform |
|---|---|
| `instagram-scout.py` -- creator discovery shortlist | Instagram |
| `instagram-competitor-watch.py` -- competitor content monitor | Instagram |
| `local-deal-scout.py` -- best Walmart deals in a category | Walmart |
| `amazon-review-miner.py` -- mine reviews for praise/complaints | Amazon |
| `youtube-course-builder.py` -- YouTube to ordered curriculum | YouTube |
| `momentum-radar.py` -- cross-platform momentum score | Multi |

| New notebook | Platform |
|---|---|
| `instagram-hashtag-analyzer.ipynb` -- rank hashtags by volume | Instagram |
| `instagram-profile-analytics.ipynb` -- engagement + theme snapshot | Instagram |
| `amazon-bestseller-rank-tracker.ipynb` -- category leaders | Amazon |
| `google-knowledge-graph-extractor.ipynb` -- structured entity facts | Google |
| `tiktok-comment-sentiment.ipynb` -- comment sentiment (SDK + LLM) | TikTok |

(Plus the original 8 agents and 14 notebooks -- see their folders.)

### Multi-agent frameworks
| Example | Framework | Platforms |
|---|---|---|
| `recipes/crewai/market-research-crew.py` | CrewAI | Google + Reddit |
| `recipes/crewai/product-launch-crew.py` | CrewAI | Amazon + Walmart + YouTube |
| `recipes/crewai/influencer-campaign-crew.py` | CrewAI | TikTok + Instagram |
| `recipes/crewai/seo-content-crew.py` | CrewAI | Google |
| `recipes/agno/agno-shopping-assistant.py` | Agno | Amazon + Walmart |
| `recipes/agno/agno-social-listener.py` | Agno | Reddit + TikTok + Instagram |
| `recipes/agno/agno-research-team.py` | Agno | Google + YouTube |
| `recipes/smolagents/smolagents-web-researcher.py` | smolagents | Google |
| `recipes/smolagents/smolagents-fact-checker.py` | smolagents | Google |
| `recipes/haystack/haystack-rag-websearch.ipynb` | Haystack | Google |
| `recipes/haystack/haystack-news-qa.py` | Haystack | Google |
| `recipes/autogen/autogen-shopping-groupchat.py` | AutoGen | Amazon + Walmart + YouTube |
| `recipes/autogen/autogen-trend-analyst.py` | AutoGen | YouTube + Reddit |

### No-code + MCP
| Example | What |
|---|---|
| `recipes/n8n/reddit-mention-to-slack.json` | Scheduled Reddit -> Slack workflow |
| `recipes/n8n/amazon-price-drop-email.json` | Scheduled Amazon price -> email workflow |
| `recipes/mcp/mcp_python_client.py` | Call the hosted Scavio MCP server from Python |
| `recipes/mcp/mcp-config.example.json` | Drop-in MCP config for Claude Desktop / Cursor |

## Using Scavio via MCP

Scavio runs a hosted MCP server at `https://mcp.scavio.dev/mcp` exposing all 33
endpoints as tools. Point any MCP client at it with your key in the `x-api-key`
header -- see [`recipes/mcp`](recipes/mcp).

## Why Scavio vs. the alternatives

| Need | Expensive tool | Scavio |
|------|----------------|--------|
| SERP + People Also Ask | SerpAPI ($75/mo) | Free (50 calls) |
| Amazon product data | Jungle Scout ($49-129/mo) | One API call |
| YouTube video metadata | VidIQ/TubeBuddy ($7-49/mo) | One API call |
| Reddit lead / GTM tracking | GummySearch ($29-99/mo) | `recipes/python-sdk/reddit_alert_watcher.py` |
| TikTok / Instagram creator discovery | Modash ($99-399/mo) | `recipes/crewai/influencer-campaign-crew.py` |
| Price tracking | Keepa / CamelCamelCamel | `recipes/python-sdk/walmart_price_logger.py` |
| Brand monitoring | Brand24 ($99-299/mo) | `recipes/vercel-ai/reddit-sentiment-tool.ts` |

## SDK cheat sheet

```python
# Python -- pip install scavio
from scavio import ScavioClient
c = ScavioClient()                       # reads SCAVIO_API_KEY
c.google.search("ai agents")
c.amazon.product("B0CHWRXH8B")           # ASIN
c.youtube.search("python tutorial")
c.reddit.search("serpapi alternative", sort="new")
c.instagram.profile(username="nike")
c.tiktok.search_users(keyword="coffee")
```

```typescript
// JS/TS -- npm install scavio
import { Scavio } from "scavio";
const c = new Scavio();                   // reads SCAVIO_API_KEY
await c.google.search({ query: "ai agents" });
await c.amazon.product({ asin: "B0CHWRXH8B" });
await c.tiktok.searchUsers({ keyword: "coffee" });
```

## FAQ

**Is this a free alternative to SerpAPI or ScraperAPI?**
Yes. 50 free real-time credits to start (one-time, no card) across Google,
Amazon, YouTube, Walmart, Reddit, TikTok, and Instagram -- enough to build and
test a project. Paid plans add monthly credits when you need more.

**Which frameworks are supported?**
LangChain, the Vercel AI SDK, CrewAI, Agno, smolagents, Haystack, and AutoGen
all have first-class Scavio tools, plus a hosted MCP server and an n8n node.
Every framework has at least one example here.

**Does it work with OpenAI, Claude, Gemini, local models?**
Yes -- the LLM is yours to choose. Examples default to OpenAI; swap freely.

**Is scraping Amazon / Instagram legal?**
You call Scavio's licensed real-time search API, not the platforms directly.
Your IP never gets blocked.

## Contributing

PRs welcome:
- One example per file; keep agents under ~200 lines, notebooks under ~15 cells.
- A docstring/markdown header with prerequisites and usage.
- Verified against the free tier. No emojis, no generated-by-AI attribution.

## Resources

- [Scavio Dashboard](https://dashboard.scavio.dev) -- free API key
- [Scavio Docs](https://scavio.dev/docs) -- REST + MCP reference
- [`scavio` on PyPI](https://pypi.org/project/scavio/) - [`scavio` on npm](https://www.npmjs.com/package/scavio)

---

**Keywords:** ai search api, serpapi alternative free, scraperapi alternative, amazon product api python, walmart api, youtube data api alternative, reddit search api, tiktok api, instagram api, langchain search tool, vercel ai sdk tools, crewai tools, agno tools, smolagents web search, haystack websearch, autogen tools, n8n scavio node, mcp search server, people also ask api, google serp api, ai shopping agent, influencer discovery api, brand monitoring api, price tracking api, retail arbitrage, seo keyword research api.

Powered by **[Scavio](https://scavio.dev)** -- the real-time search API for AI agents.
