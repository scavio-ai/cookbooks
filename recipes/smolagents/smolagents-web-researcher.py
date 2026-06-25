"""
smolagents web researcher - grounded answers with sources via Scavio Google search.

A free, self-hosted alternative to paid web-research APIs (Tavily, SerpAPI): a
smolagents CodeAgent that researches any question through Scavio's Google web
search endpoint and returns a grounded answer with the source links it used.

Prerequisites:
    pip install smolagents scavio openai python-dotenv
    export SCAVIO_API_KEY=...   # free key: https://dashboard.scavio.dev
    export OPENAI_API_KEY=...

Usage:
    python smolagents-web-researcher.py "What is the latest model from Mistral AI?"
"""

import os
import sys

from dotenv import load_dotenv

from smolagents import CodeAgent, OpenAIServerModel

from scavio_search_tool import ScavioSearchTool

load_dotenv(override=True)


def main() -> None:
    question = " ".join(sys.argv[1:]) or "What is the latest model from Mistral AI?"

    model = OpenAIServerModel(model_id="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])
    agent = CodeAgent(tools=[ScavioSearchTool(max_results=5)], model=model)

    answer = agent.run(
        "Research this question using the web_search tool, then write a concise, "
        "grounded answer. End with a 'Sources:' list of the URLs you relied on.\n\n"
        f"Question: {question}"
    )

    print("\n=== Answer ===\n")
    print(answer)


if __name__ == "__main__":
    main()
