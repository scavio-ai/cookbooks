# CrewAI recipes

Multi-agent crews built on [CrewAI](https://github.com/crewAIInc/crewAI) and
the [`crewai-scavio`](https://pypi.org/project/crewai-scavio/) tools. Each
crew uses the [Scavio Search API](https://scavio.dev/docs/introduction) for
live web, retail, and social data through a single API key -- no scraping,
proxies, or per-source keys. Every script is a self-contained CLI.

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

| Script | What it does | Scavio tools |
|---|---|---|
| `market-research-crew.py` | 3-agent crew that produces a market-research brief for a niche | Google Search, Reddit Search |
| `product-launch-crew.py` | Competitive crew that analyzes rivals before a product launch | Amazon Search, Walmart Search, YouTube Search |
| `influencer-campaign-crew.py` | Crew that builds a TikTok + Instagram creator shortlist for a campaign | TikTok Search (users/videos), Instagram Search (users/hashtags) |
| `seo-content-crew.py` | Crew that mines the SERP and writes an SEO content plan for a seed keyword | Google Search |

## Run

```bash
python market-research-crew.py "AI note-taking apps for students"
python product-launch-crew.py "stainless steel insulated water bottle"
python influencer-campaign-crew.py "sustainable activewear for runners"
python seo-content-crew.py "home espresso machines"
```

Each script takes its topic as command-line arguments and prints the final
crew output. Swap the `MODEL` constant in any file to use a different LLM.
