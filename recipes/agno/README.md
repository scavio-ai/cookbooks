# Agno recipes

[Agno](https://github.com/agno-agi/agno) agents that use the unified
[Scavio API](https://scavio.dev) (Google, YouTube, Amazon, Walmart, Reddit,
TikTok, Instagram) as a free, self-hosted alternative to paid
search/research/social-listening tools.

> **Get a free Scavio API key (250 credits/month, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
```

All examples use OpenAI `gpt-4o-mini` and read keys from the environment (or a
`.env` file via `python-dotenv`).

## Recipes

- **`agno-shopping-assistant.py`** -- compares a product on Amazon vs Walmart and
  recommends the better deal. Powered by the [Scavio Amazon + Walmart APIs](https://scavio.dev) --
  [get a free key](https://dashboard.scavio.dev).
- **`agno-social-listener.py`** -- listens across Reddit, TikTok, and Instagram and
  summarizes sentiment about a brand/topic. Built on the [Scavio social APIs](https://scavio.dev) --
  a free [Brand24 alternative](https://dashboard.scavio.dev).
- **`agno-research-team.py`** -- researches a topic across articles and videos into
  a structured briefing. Uses the [Scavio Google + YouTube APIs](https://scavio.dev) --
  [start free](https://dashboard.scavio.dev).

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
Its `youtube_search` and `tiktok_search_videos` wrappers compact the (very
large) raw payloads down to the useful fields, so multi-source agents stay well
within the model's context window.

---

Build real-time search agents with **[Scavio](https://scavio.dev)** -- [read the docs](https://scavio.dev/docs).
