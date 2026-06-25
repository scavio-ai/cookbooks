"""
AutoGen trend analyst - topic momentum across YouTube and Reddit.

A free, self-hosted alternative to paid social-listening and trend-tracking
APIs: a Microsoft AutoGen AssistantAgent wired with Scavio's YouTube and Reddit
search tools. It gauges whether a topic is gaining or losing momentum by
reading recent video coverage and community discussion.

Prerequisites:
    pip install autogen-scavio autogen-agentchat autogen-ext[openai] python-dotenv
    export SCAVIO_API_KEY=...   # free key: https://dashboard.scavio.dev
    export OPENAI_API_KEY=...

Usage:
    python autogen-trend-analyst.py "ai coding agents"
"""

import asyncio
import sys

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_scavio import (
    create_reddit_search_tool,
    create_youtube_search_tool,
)

load_dotenv(override=True)


async def main() -> None:
    topic = " ".join(sys.argv[1:]) or "ai coding agents"

    # YouTube search returns large raw payloads (thumbnail variants, rich
    # metadata); a handful of results can exceed gpt-4o-mini's 128k context once
    # they accumulate across tool-call rounds. Keep YouTube results small so the
    # transcript stays within context; Reddit payloads are lighter.
    tools = [
        create_youtube_search_tool(max_results=2),
        create_reddit_search_tool(max_results=5),
    ]

    # Scavio's free/pay-as-you-go plans allow one in-flight request at a time,
    # so we disable parallel tool calls and let the agent query each source
    # sequentially. max_tool_iterations gives it room for several search rounds
    # before it must answer.
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        parallel_tool_calls=False,
    )

    agent = AssistantAgent(
        name="trend_analyst",
        model_client=model_client,
        tools=tools,
        reflect_on_tool_use=True,
        max_tool_iterations=6,
        system_message=(
            "You are a trend analyst. Use YouTube search (sort_by 'view_count' "
            "or 'relevance') and Reddit search (sort by new and top) to gauge a "
            "topic's momentum. Judge whether interest is rising, flat, or "
            "fading, and back the call with specific video titles, view counts, "
            "subreddits, and post titles you actually found. End with a "
            "one-line verdict: RISING, STEADY, or COOLING."
        ),
    )

    task = (
        f"Analyze the current momentum of '{topic}'. Check recent YouTube "
        f"videos and Reddit discussion, then judge whether it is rising, "
        f"steady, or cooling."
    )

    result = await agent.run(task=task)
    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(main())
