"""Answer a current-events question from live web search, with cited sources.

A free alternative to paid web-search / answer-engine tools: Scavio's unified
Search API provides the live Google results, Haystack's OpenAIGenerator turns
them into a grounded answer, and every claim is backed by source URLs.

Prerequisites
-------------
    pip install scavio-haystack haystack-ai openai python-dotenv

Environment variables (a .env file in the cookbook root works too):
    SCAVIO_API_KEY   free key at https://dashboard.scavio.dev
    OPENAI_API_KEY   for gpt-4o-mini

Usage
-----
    python haystack-news-qa.py "who won the latest f1 grand prix"

If no question is passed on the command line, a default one is used.
"""

import sys

from dotenv import load_dotenv
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret

from haystack_integrations.components.websearch.scavio import ScavioWebSearch

load_dotenv(override=True)

PROMPT = """\
You are a current-events assistant. Using ONLY the web search results below,
answer the question. Be concise and factual. If the results do not contain the
answer, say so plainly. Do not invent facts.

Web search results:
{% for doc in documents %}
[{{ loop.index }}] {{ doc.meta["title"] }} ({{ doc.meta["url"] }})
{{ doc.content }}
{% endfor %}

Question: {{ query }}
Answer:"""


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() or "What are the latest developments in AI this week?"

    web_search = ScavioWebSearch(api_key=Secret.from_env_var("SCAVIO_API_KEY"), top_k=6)
    prompt_builder = PromptBuilder(template=PROMPT, required_variables=["documents", "query"])
    llm = OpenAIGenerator(model="gpt-4o-mini")

    print(f"Searching the web for: {query}\n")
    search = web_search.run(query=query)
    documents = search["documents"]
    links = search["links"]

    if not documents:
        print("No web results found. Try a different question.")
        return

    prompt = prompt_builder.run(documents=documents, query=query)["prompt"]
    answer = llm.run(prompt=prompt)["replies"][0]

    print("Answer\n------")
    print(answer)
    print("\nSources\n-------")
    for i, url in enumerate(links, 1):
        print(f"[{i}] {url}")


if __name__ == "__main__":
    main()
