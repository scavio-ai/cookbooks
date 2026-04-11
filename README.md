# Scavio Cookbook -- 10 AI Agents You Can Build Today

Open-source AI agents powered by [Scavio](https://scavio.dev) -- the real-time search API for Google, Amazon, YouTube, and Walmart.

Each agent is a complete, working example you can run, learn from, and adapt for your own projects.

**500 free API credits/month. No credit card required.** [Get your key](https://dashboard.scavio.dev)

## Agents

| # | Agent | Level | What it does | Tools |
|---|-------|-------|-------------|-------|
| 1 | [FlipFinder](agents/flipfinder/) | Advanced | Find products to buy on Walmart and resell on Amazon for profit | 6 |
| 2 | [YouTubeScholar](agents/youtubescholar/) | Beginner | Build free course curricula from YouTube videos | 3 |
| 3 | [ReviewGuard](agents/reviewguard/) | Intermediate | Detect fake Amazon reviews by cross-referencing YouTube | 5 |
| 4 | [DealStack](agents/dealstack/) | Intermediate | Build the cheapest shopping cart across Amazon + Walmart | 4 |
| 5 | [ContentRadar](agents/contentradar/) | Intermediate | Find SEO content gaps your competitors missed | 1 |
| 6 | [BuyWise](agents/buywise/) | Intermediate | Compare products across Amazon, Walmart, and YouTube reviews | 5 |
| 7 | [NicheHunter](agents/nichehunter/) | Advanced | Find trending products before they blow up | 5 |
| 8 | [TubeToPost](agents/tubetopost/) | Beginner | Turn any YouTube video into an SEO-optimized blog post | 3 |
| 9 | [BrandSpy](agents/brandspy/) | Advanced | Free alternative to $300/month brand monitoring tools | 5 |
| 10 | [DebateSettler](agents/debatesettler/) | Intermediate | Research both sides of any argument with real sources | 4 |

## Learning Path

New to Scavio? Follow this path:

1. **Start here** -- [Getting Started](getting-started/) -- make your first API call in 5 minutes
2. **Beginner** -- [YouTubeScholar](agents/youtubescholar/) or [TubeToPost](agents/tubetopost/) -- learn 3 YouTube tools
3. **Intermediate** -- [ReviewGuard](agents/reviewguard/) or [DealStack](agents/dealstack/) -- cross-platform searches
4. **Advanced** -- [FlipFinder](agents/flipfinder/) or [NicheHunter](agents/nichehunter/) -- multi-tool orchestration

## Frameworks

Each agent is implemented in multiple frameworks so you can use what you know:

| Framework | Description | Setup |
|-----------|-------------|-------|
| **[Agno](https://github.com/agno-agi/agno)** | Lightweight Python agent framework (39k stars). Connects to Scavio via MCP. | `pip install agno` |
| **[LangChain](https://github.com/langchain-ai/langchain)** | Enterprise AI framework. Uses [langchain-scavio](https://pypi.org/project/langchain-scavio/) for direct API access. | `pip install langchain-scavio` |
| **[CrewAI](https://github.com/crewAIInc/crewAI)** | Multi-agent orchestration (45k stars). Used for agents with multiple AI roles. | `pip install crewai` |

All agents support both **OpenAI** (GPT-4o) and **Anthropic** (Claude) as the LLM.

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/scavio-dev/cookbook.git
cd cookbook

# 2. Pick an agent (e.g., FlipFinder with Agno)
cd agents/flipfinder/agno

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API keys
cp .env.example .env
# Edit .env with your Scavio key (free) and OpenAI/Anthropic key

# 5. Run it
python main.py "kitchen gadgets"
```

## Scavio Tools Reference

These 9 tools are available in every agent via MCP or REST API:

| Tool | Platform | What it does |
|------|----------|-------------|
| `search_google` | Google | Web search with results, news, PAA, knowledge graph |
| `search_amazon` | Amazon | Product search with price, rating, and category filters |
| `get_amazon_product` | Amazon | Full product details by ASIN |
| `search_walmart` | Walmart | Product search with price, fulfillment, and delivery filters |
| `get_walmart_product` | Walmart | Full product details by product ID |
| `search_youtube` | YouTube | Video, channel, and playlist search |
| `get_youtube_metadata` | YouTube | Video title, views, likes, duration |
| `get_youtube_transcript` | YouTube | Full timestamped video transcripts |
| `get_usage` | Scavio | Check credit balance and plan details |

## Two Ways to Connect

**MCP (for AI agents):** Connect to `https://mcp.scavio.dev/mcp` with your API key. Tools are auto-discovered.

**REST API (for apps):** POST to `https://api.scavio.dev/api/v1/{endpoint}` with Bearer auth. Returns JSON.

See [Getting Started](getting-started/) for setup instructions for both methods.

## Contributing

Found a bug? Want to add a new agent? PRs welcome.

- Each agent should be a single file under 200 lines
- Include a README with demo output and "Build Your Own" section
- Test with the free tier (500 credits)

## Links

- [Scavio Docs](https://scavio.dev/docs) -- API reference
- [Scavio Dashboard](https://dashboard.scavio.dev) -- Get your free API key
- [Scavio Blog](https://scavio.dev/blog) -- Tutorials and guides
- [langchain-scavio on PyPI](https://pypi.org/project/langchain-scavio/) -- LangChain integration

---

**Powered by [Scavio](https://scavio.dev)** -- Real-time search API for AI agents. 500 free credits/month.
