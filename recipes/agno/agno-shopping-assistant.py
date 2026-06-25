"""
Agno shopping assistant - Amazon vs Walmart price comparison.

A free, self-hosted alternative to paid shopping-research APIs: an Agno agent
that searches both Amazon and Walmart through Scavio's unified Search API and
returns a side-by-side comparison with concrete prices and a recommendation.

Prerequisites:
    pip install agno scavio openai python-dotenv
    export SCAVIO_API_KEY=...   # free key: https://dashboard.scavio.dev
    export OPENAI_API_KEY=...

Usage:
    python agno-shopping-assistant.py "wireless noise cancelling headphones"
"""

import sys

from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from scavio_toolkit import ScavioTools

load_dotenv(override=True)


def main() -> None:
    product = " ".join(sys.argv[1:]) or "wireless noise cancelling headphones"

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ScavioTools(enable_amazon=True, enable_walmart=True)],
        instructions=[
            "You are a shopping assistant.",
            "Search Amazon AND Walmart for the requested product.",
            "Compare the top matches on price, then recommend the better buy.",
            "Always cite the actual product titles and prices you found.",
        ],
        markdown=True,
    )

    agent.print_response(
        f"Compare prices for '{product}' on Amazon vs Walmart and tell me which is the better deal.",
        markdown=True,
    )


if __name__ == "__main__":
    main()
