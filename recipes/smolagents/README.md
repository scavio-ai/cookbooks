# smolagents + Scavio

Hugging Face [smolagents](https://github.com/huggingface/smolagents) examples that
give an agent live web search through [Scavio](https://scavio.dev), a unified search
API for AI agents. Both examples use the Google web search endpoint as a free,
self-hosted alternative to paid web-research tools.

> **Get a free Scavio API key (250 credits/month, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Examples

- **`smolagents-web-researcher.py`** -- a CodeAgent that researches a question
  and returns a grounded answer with source links. Powered by the
  [Scavio web search API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`smolagents-fact-checker.py`** -- a CodeAgent that takes a claim and returns
  a verdict (supported / refuted / unclear) with evidence. Built on the
  [Scavio Google Search API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).

`scavio_search_tool.py` is the vendored Scavio search tool (`ScavioSearchTool`). It is
a single-file tool, not a PyPI package, so it lives in this folder and is imported
directly by both examples.

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY=...   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY=...
```

You can also put `SCAVIO_API_KEY` and `OPENAI_API_KEY` in a `.env` file; the examples
load it with `python-dotenv`.

## Run

```bash
python smolagents-web-researcher.py "What is the latest model from Mistral AI?"
python smolagents-fact-checker.py "The Eiffel Tower is taller than the Empire State Building"
```

---

Give your smolagents real-time web search with **[Scavio](https://scavio.dev)** -- [read the docs](https://scavio.dev/docs).
