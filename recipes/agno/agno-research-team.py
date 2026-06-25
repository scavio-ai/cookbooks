"""
Agno research agent - Google + YouTube topic briefing.

A free, self-hosted alternative to paid research APIs: an Agno agent that
researches a topic using both Google web search and YouTube video search
through Scavio's unified Search API, then writes a structured briefing that
blends written sources with relevant videos.

Prerequisites:
    pip install agno scavio openai python-dotenv
    export SCAVIO_API_KEY=...   # free key: https://dashboard.scavio.dev
    export OPENAI_API_KEY=...

Usage:
    python agno-research-team.py "the topic to research"
"""

import sys

from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from scavio_toolkit import ScavioTools

load_dotenv(override=True)


def main() -> None:
    topic = " ".join(sys.argv[1:]) or "the state of open-source AI agent frameworks in 2026"

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ScavioTools(enable_google=True, enable_youtube=True)],
        instructions=[
            "You are a research analyst.",
            "Research the topic using BOTH Google web search and YouTube video search.",
            "Cross-reference what you find in articles against what creators say in videos.",
            "Write a structured briefing with: a short summary, key findings (with sources), "
            "and a list of recommended videos (title + why it is useful).",
            "Cite the real URLs and titles you retrieved.",
        ],
        markdown=True,
    )

    agent.print_response(
        f"Research this topic and write a briefing: {topic}",
        markdown=True,
    )


if __name__ == "__main__":
    main()
