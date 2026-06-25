"""
smolagents fact checker - verify a claim against the live web via Scavio Google search.

A free, self-hosted alternative to paid fact-checking APIs: a smolagents CodeAgent
that takes a claim, searches Google through Scavio's unified Search API, and returns
a verdict (supported / refuted / unclear) backed by the evidence it found.

Prerequisites:
    pip install smolagents scavio openai python-dotenv
    export SCAVIO_API_KEY=...   # free key: https://dashboard.scavio.dev
    export OPENAI_API_KEY=...

Usage:
    python smolagents-fact-checker.py "The Eiffel Tower is taller than the Empire State Building"
"""

import os
import sys

from dotenv import load_dotenv

from smolagents import CodeAgent, OpenAIServerModel

from scavio_search_tool import ScavioSearchTool

load_dotenv(override=True)


def main() -> None:
    claim = " ".join(sys.argv[1:]) or "The Eiffel Tower is taller than the Empire State Building"

    model = OpenAIServerModel(model_id="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])
    agent = CodeAgent(tools=[ScavioSearchTool(max_results=5)], model=model)

    verdict = agent.run(
        "Fact-check the claim below using the web_search tool. Search for evidence, "
        "then return a final answer in this exact shape:\n"
        "Verdict: <SUPPORTED | REFUTED | UNCLEAR>\n"
        "Reasoning: <one or two sentences>\n"
        "Evidence: <bullet list of source URLs that justify the verdict>\n\n"
        f"Claim: {claim}"
    )

    print("\n=== Fact Check ===\n")
    print(verdict)


if __name__ == "__main__":
    main()
