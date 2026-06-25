# Haystack recipes

[Haystack](https://haystack.deepset.ai) pipelines that use the
[Scavio API](https://scavio.dev) for live Google web search -- a free
alternative to paid web-search and answer engines (Tavily, Exa, SerpAPI). The
[`scavio-haystack`](https://pypi.org/project/scavio-haystack/) package ships a
`ScavioWebSearch` component returning Haystack `Document`s plus source links.

> **Get a free Scavio API key (250 credits/month, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
```

Both examples use OpenAI `gpt-4o-mini` and read keys from the environment (or a
`.env` via `python-dotenv`).

## Recipes

- **`haystack-rag-websearch.ipynb`** -- a web-search RAG `Pipeline`
  (`ScavioWebSearch` -> `PromptBuilder` -> `OpenAIGenerator`) answering grounded
  in live results. Powered by the [Scavio web search API](https://scavio.dev) --
  a free [Tavily alternative](https://dashboard.scavio.dev).
- **`haystack-news-qa.py`** -- answers a current-events question with cited
  source URLs. Built on the [Scavio Google Search API](https://scavio.dev) --
  [get a free key](https://dashboard.scavio.dev).

```bash
python haystack-news-qa.py "who won the latest f1 grand prix"
```

---

Add live web search to your Haystack pipelines with **[Scavio](https://scavio.dev)** -- [scavio-haystack on PyPI](https://pypi.org/project/scavio-haystack/).
