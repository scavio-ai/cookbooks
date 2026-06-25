# AutoGen recipes

Microsoft [AutoGen](https://github.com/microsoft/autogen) agents that use
Scavio's unified Search API (Google, YouTube, Amazon, Walmart, Reddit, TikTok,
Instagram) as a free, self-hosted alternative to paid shopping-research and
social-listening tools.

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

| Script | What it does | Providers |
|---|---|---|
| `autogen-shopping-groupchat.py` | Compares a product across Amazon and Walmart, factors in YouTube review coverage, and recommends one purchase | Amazon, Walmart, YouTube |
| `autogen-trend-analyst.py` | Gauges a topic's momentum (rising / steady / cooling) from recent YouTube videos and Reddit discussion | YouTube, Reddit |

Each takes the query as a command-line argument, e.g.:

```bash
python autogen-shopping-groupchat.py "wireless noise cancelling headphones"
python autogen-trend-analyst.py "ai coding agents"
```
