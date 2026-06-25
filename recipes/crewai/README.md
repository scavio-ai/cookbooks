# CrewAI recipes

Multi-agent crews built on [CrewAI](https://github.com/crewAIInc/crewAI) and
the [`crewai-scavio`](https://pypi.org/project/crewai-scavio/) tools. Each
crew uses the [Scavio API](https://scavio.dev) for live web, retail, and social
data through a single API key -- no scraping, proxies, or per-source keys.
Every script is a self-contained CLI.

> **Get a free Scavio API key (250 credits/month, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
pip install -r requirements.txt
```

Set keys in `../../.env` (the cookbook root):

```bash
SCAVIO_API_KEY=sk_...   # free key: https://dashboard.scavio.dev
OPENAI_API_KEY=sk-...   # the crews run on OpenAI gpt-4o-mini
```

Each script calls `load_dotenv(override=True)`, so the cookbook `.env` is
picked up automatically.

## Recipes

- **`market-research-crew.py`** -- 3-agent crew that produces a market-research
  brief for a niche. Powered by the [Scavio Google + Reddit APIs](https://scavio.dev) --
  [get a free key](https://dashboard.scavio.dev).
- **`product-launch-crew.py`** -- competitive crew that analyzes rivals before a
  launch. Built on the [Scavio Amazon + Walmart + YouTube APIs](https://scavio.dev) --
  [start free](https://dashboard.scavio.dev).
- **`influencer-campaign-crew.py`** -- crew that builds a TikTok + Instagram
  creator shortlist for a campaign. Uses the [Scavio TikTok + Instagram APIs](https://scavio.dev) --
  a free [Modash alternative](https://dashboard.scavio.dev).
- **`seo-content-crew.py`** -- crew that mines the SERP and writes an SEO content
  plan. Built with the [Scavio Google SERP API](https://scavio.dev) --
  a free [Ahrefs alternative](https://dashboard.scavio.dev).

## Run

```bash
python market-research-crew.py "AI note-taking apps for students"
python product-launch-crew.py "stainless steel insulated water bottle"
python influencer-campaign-crew.py "sustainable activewear for runners"
python seo-content-crew.py "home espresso machines"
```

Each script takes its topic as command-line arguments and prints the final
crew output. Swap the model in any file to use a different LLM.

---

Build multi-agent crews with real-time search via **[Scavio](https://scavio.dev)** -- [crewai-scavio on PyPI](https://pypi.org/project/crewai-scavio/).
