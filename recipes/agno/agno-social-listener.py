"""
Agno social listener - cross-platform brand sentiment.

A free, self-hosted alternative to paid social-listening tools: an Agno agent
that monitors what people say about a brand or topic across Reddit, TikTok, and
Instagram via Scavio's unified Search API, then summarizes the chatter and
overall sentiment.

Prerequisites:
    pip install agno scavio openai python-dotenv
    export SCAVIO_API_KEY=...   # free key: https://dashboard.scavio.dev
    export OPENAI_API_KEY=...

Usage:
    python agno-social-listener.py "your brand or topic"
"""

import sys

from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from scavio_toolkit import ScavioTools

load_dotenv(override=True)


def main() -> None:
    topic = " ".join(sys.argv[1:]) or "Notion AI"

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[
            ScavioTools(
                enable_reddit=True,
                enable_tiktok=True,
                enable_instagram=True,
            )
        ],
        instructions=[
            "You are a social listening analyst.",
            "Use Reddit search, TikTok video search, and Instagram hashtag/user search "
            "to find what people are saying about the topic.",
            "Summarize the main themes, notable posts, and overall sentiment "
            "(positive / negative / mixed).",
            "Quote real posts or comments and name the platform each came from.",
        ],
        markdown=True,
    )

    agent.print_response(
        f"What are people saying about '{topic}' across Reddit, TikTok, and Instagram? "
        "Summarize the themes and the overall sentiment.",
        markdown=True,
    )


if __name__ == "__main__":
    main()
