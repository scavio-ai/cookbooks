# Scavio Cookbook: Open-Source LangChain Agents for Amazon, Google, YouTube & Walmart

**Production-ready AI agent examples** that search Amazon products, Google results, YouTube videos, and Walmart listings in real time -- built with [LangChain](https://github.com/langchain-ai/langchain) and powered by the [Scavio](https://scavio.dev) search API.

[![PyPI](https://img.shields.io/pypi/v/langchain-scavio.svg?label=langchain-scavio)](https://pypi.org/project/langchain-scavio/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Scavio](https://img.shields.io/badge/powered%20by-Scavio-ff4d00.svg)](https://scavio.dev)

> **500 free API credits every month. No credit card required.** [Get your free key in 30 seconds](https://dashboard.scavio.dev)

---

## What's inside

- **Working AI agents** you can `git clone` and run in under 5 minutes
- **Real search APIs** -- not scrapers, not mocks -- Amazon, Google, YouTube transcripts, Walmart
- **LangChain `create_agent` examples** with tool calling, multi-step reasoning, and grounded outputs
- **Free alternative** to SerpAPI, ScraperAPI, Bright Data, Jungle Scout, Fakespot, and $149/month SEO tools

## Quick Start (5 minutes)

```bash
git clone https://github.com/scavio-ai/cookbooks.git
cd cookbooks

python -m venv .venv
source .venv/bin/activate
pip install langchain langchain-openai langchain-scavio python-dotenv

cp .env.example .env
# Edit .env with SCAVIO_API_KEY (free) and OPENAI_API_KEY

python agents/amazon-agent.py "best wired earbuds under $50"
```

Output:

```
Top Pick: Skullcandy Jib Wired Earbuds (ASIN: B075F6TB7F)
- Rationale: $7.99, 4.4 stars from ~20k reviews, noise-isolating fit.
- Red Flag: Some users report volume control issues.

Runner-Up: Apple EarPods with Lightning (ASIN: B0D7FVQ1ZB)
- Rationale: $15.98, 4.6 stars from ~14k reviews, reliable Apple fit.
- Red Flag: May not fit all ear sizes; sound leakage at high volume.
```

## Agent Catalog

| # | Agent | Use Case | Status |
|---|-------|----------|--------|
| 1 | [AmazonScout](agents/amazon-agent.py) | Amazon product research with grounded recommendations | **Shipped** |
| 2 | YouTubeScholar | Turn YouTube videos into a free course curriculum | Coming soon |
| 3 | ReviewGuard | Detect fake Amazon reviews by cross-referencing YouTube | Coming soon |
| 4 | DealStack | Cheapest shopping cart across Amazon and Walmart | Coming soon |
| 5 | ContentRadar | Find SEO content gaps your competitors missed | Coming soon |
| 6 | BuyWise | Compare products across Amazon, Walmart, and YouTube reviews | Coming soon |
| 7 | NicheHunter | Find trending products before they blow up | Coming soon |
| 8 | TubeToPost | Turn any YouTube video into an SEO-optimized blog post | Coming soon |
| 9 | BrandSpy | Free alternative to $300/month brand monitoring tools | Coming soon |
| 10 | FlipFinder | Retail arbitrage: buy on Walmart, resell on Amazon | Coming soon |

All agents are **single-file, under 200 lines, MIT licensed**. Fork, adapt, ship.

## Why Scavio vs. the alternatives

| Need | Expensive tool | Scavio + LangChain |
|------|----------------|---------------------|
| Amazon product search API | Jungle Scout ($49-129/mo) | Free (500 calls/mo) |
| SERP + People Also Ask | SerpAPI ($75/mo) | Free (500 calls/mo) |
| YouTube transcripts | Whisper + scraping | One API call |
| Fake review detection | Fakespot Premium | Cross-reference YouTube reviews for free |
| Brand monitoring | Brand24 ($99-299/mo) | Free with BrandSpy agent |
| SEO content gap analysis | Ahrefs ($99-449/mo) | Free with ContentRadar agent |

## LangChain Tools Reference

Install once -- every agent uses the same tools via [langchain-scavio](https://pypi.org/project/langchain-scavio/):

```python
from langchain_scavio import (
    ScavioSearch,              # Google search: results, news, PAA, knowledge graph
    ScavioAmazonSearch,        # Amazon product search
    ScavioAmazonProduct,       # Amazon product details by ASIN
    ScavioWalmartSearch,       # Walmart product search
    ScavioWalmartProduct,      # Walmart product details
    ScavioYouTubeSearch,       # YouTube video, channel, playlist search
    ScavioYouTubeMetadata,     # YouTube video metadata
    ScavioYouTubeTranscript,   # Full timestamped YouTube transcripts
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
Yes. Scavio gives you 500 free real-time search credits per month across Google, Amazon, YouTube, and Walmart -- enough to build and ship most personal projects or MVPs.

**Does it work with OpenAI GPT-4o, Claude, and other LLMs?**
Yes. Every agent uses LangChain's `create_agent`, so you can swap in any chat model: OpenAI, Anthropic Claude, Google Gemini, Groq, local Ollama models, etc.

**Can I use this for e-commerce price monitoring or dropshipping research?**
Yes. The Amazon + Walmart tools return live pricing, stock, ratings, ASINs, and reviews. See the NicheHunter, FlipFinder, and DealStack agents for examples.

**How do I get YouTube video transcripts?**
Use `ScavioYouTubeTranscript` -- one call returns the full timestamped transcript of any public YouTube video, ready to pipe into any LLM.

**Is scraping Amazon legal?**
Scavio is a licensed real-time search provider -- you call Scavio's API, not Amazon's. Your agent stays compliant and your IP never gets blocked.

## Contributing

PRs welcome. Guidelines:

- One agent per file, under 200 lines
- Short docstring with prerequisites and usage
- Verified against the free tier (500 credits/month)
- No emojis, no generated-by-AI attribution

## Resources

- [Scavio Dashboard](https://dashboard.scavio.dev) -- free API key
- [Scavio Docs](https://scavio.dev/docs) -- REST + MCP reference
- [langchain-scavio on PyPI](https://pypi.org/project/langchain-scavio/)
- [LangChain Agents Guide](https://docs.langchain.com/oss/python/langchain/agents)

---

**Keywords:** langchain amazon api, langchain youtube transcript, amazon product search api python, free serpapi alternative, ai shopping agent, langchain agent examples, amazon scraper api free, youtube transcript langchain tool, walmart api langchain, ai agent cookbook, openai amazon agent, gpt-4 shopping assistant, langchain tool calling examples, free amazon product api, ai price comparison agent, fake review detector open source, ai seo content gap finder, brand monitoring open source, retail arbitrage tool open source, people also ask api, google serp api free.

Powered by **[Scavio](https://scavio.dev)** -- the real-time search API for AI agents.
