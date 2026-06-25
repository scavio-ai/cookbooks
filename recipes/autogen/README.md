# AutoGen recipes

Microsoft [AutoGen](https://github.com/microsoft/autogen) agents that use the
unified [Scavio API](https://scavio.dev) (Google, YouTube, Amazon, Walmart,
Reddit, TikTok, Instagram) as a free, self-hosted alternative to paid
shopping-research and social-listening tools.

> **Get a free Scavio API key (250 credits/month, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

These examples use the `autogen-scavio` package, which exposes Scavio endpoints
as AutoGen `FunctionTool` factories (`create_amazon_search_tool`,
`create_youtube_search_tool`, ...). They follow the AutoGen 0.4+ API:
`AssistantAgent` from `autogen-agentchat` with an `OpenAIChatCompletionClient`
from `autogen-ext`.

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
```

All examples use OpenAI `gpt-4o-mini` and read keys from the environment (or a
`.env` file via `python-dotenv`).

## Recipes

- **`autogen-shopping-groupchat.py`** -- compares a product across Amazon and
  Walmart, factors in YouTube review coverage, and recommends one purchase.
  Powered by the [Scavio retail + YouTube APIs](https://scavio.dev) --
  [get a free key](https://dashboard.scavio.dev).
- **`autogen-trend-analyst.py`** -- gauges a topic's momentum (rising / steady /
  cooling) from YouTube videos and Reddit discussion. Built on the
  [Scavio YouTube + Reddit APIs](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).

Each takes the query as a command-line argument, e.g.:

```bash
python autogen-shopping-groupchat.py "wireless noise cancelling headphones"
python autogen-trend-analyst.py "ai coding agents"
```

---

Give your AutoGen agents real-time search with **[Scavio](https://scavio.dev)** -- [autogen-scavio on PyPI](https://pypi.org/project/autogen-scavio/).
