# Agno recipes

[Agno](https://github.com/agno-agi/agno) agents that use Scavio's unified
Search API (Google, YouTube, Amazon, Walmart, Reddit, TikTok, Instagram) as a
free, self-hosted alternative to paid search/research/social-listening tools.

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
```

All examples use OpenAI `gpt-4o-mini` and read keys from the environment (or a
`.env` file via `python-dotenv`).

## Recipes

| Script | What it does | Providers |
|---|---|---|
| `agno-shopping-assistant.py` | Compares a product on Amazon vs Walmart and recommends the better deal | Amazon, Walmart |
| `agno-social-listener.py` | Listens for what people say about a brand/topic and summarizes sentiment | Reddit, TikTok, Instagram |
| `agno-research-team.py` | Researches a topic across articles and videos into a structured briefing | Google, YouTube |

Each takes the query as a command-line argument, e.g.:

```bash
python agno-shopping-assistant.py "wireless noise cancelling headphones"
```

## Note on `scavio_toolkit.py`

`scavio_toolkit.py` is the vendored Agno toolkit (`ScavioTools`). Agno's
convention is native, in-repo toolkits rather than a separate PyPI package, so
the toolkit ships as a single file. It is named `scavio_toolkit.py` (not
`scavio.py`) so it does not shadow the `scavio` SDK package it imports.
`ScavioTools` exposes every Scavio endpoint, each gated by an `enable_*` flag.
