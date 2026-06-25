"""
AutoGen shopping assistant - cross-retailer product recommendation.

A free, self-hosted alternative to paid shopping-research APIs: a Microsoft
AutoGen AssistantAgent wired with Scavio's Amazon, Walmart, and YouTube search
tools. It searches both retailers for the requested product, pulls in YouTube
review coverage, and recommends a single purchase with concrete prices.

Prerequisites:
    pip install autogen-scavio autogen-agentchat autogen-ext[openai] python-dotenv
    export SCAVIO_API_KEY=...   # free key: https://dashboard.scavio.dev
    export OPENAI_API_KEY=...

Usage:
    python autogen-shopping-groupchat.py "wireless noise cancelling headphones"
"""

import asyncio
import sys

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_scavio import (
    create_amazon_search_tool,
    create_walmart_search_tool,
    create_youtube_search_tool,
)

load_dotenv(override=True)


async def main() -> None:
    product = " ".join(sys.argv[1:]) or "wireless noise cancelling headphones"

    tools = [
        create_amazon_search_tool(max_results=4),
        create_walmart_search_tool(max_results=4),
        create_youtube_search_tool(max_results=3),
    ]

    # Scavio's free/pay-as-you-go plans allow one in-flight request at a time,
    # so we disable parallel tool calls and let the agent search each retailer
    # sequentially. max_tool_iterations gives it room for several search rounds
    # before it must answer.
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        parallel_tool_calls=False,
    )

    agent = AssistantAgent(
        name="shopping_assistant",
        model_client=model_client,
        tools=tools,
        reflect_on_tool_use=True,
        max_tool_iterations=6,
        system_message=(
            "You are a shopping assistant. Search Amazon AND Walmart for the "
            "requested product, then check YouTube for review coverage. "
            "Compare the top matches on price and recommend one product to buy. "
            "Always cite the actual product titles, prices, and retailers you "
            "found, and name a YouTube review if one is relevant."
        ),
    )

    task = (
        f"Find the best '{product}' to buy. Compare Amazon and Walmart on "
        f"price, factor in YouTube review coverage, and recommend one purchase."
    )

    result = await agent.run(task=task)
    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(main())
