# Haystack recipes

[Haystack](https://haystack.deepset.ai) pipelines that use Scavio's unified
Search API for live Google web search, as a free alternative to paid web-search
and answer-engine tools (Tavily, Exa, SerpAPI). The `scavio-haystack` package
ships a `ScavioWebSearch` component that returns results as Haystack
`Document` objects plus the list of source links.

## Setup

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
```

Both examples use OpenAI `gpt-4o-mini` and read keys from the environment (or a
`.env` file via `python-dotenv`).

## Recipes

| File | What it does | Components |
|---|---|---|
| `haystack-rag-websearch.ipynb` | A web-search RAG `Pipeline` wiring `ScavioWebSearch` to `PromptBuilder` to `OpenAIGenerator` to answer a question grounded in live web results | ScavioWebSearch, PromptBuilder, OpenAIGenerator |
| `haystack-news-qa.py` | Answers a current-events question taken from the command line, citing the source URLs | ScavioWebSearch, PromptBuilder, OpenAIGenerator |

Run the script with a question:

```bash
python haystack-news-qa.py "who won the latest f1 grand prix"
```
