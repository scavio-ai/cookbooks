"""
Product-launch competitive crew: a free alternative to paid competitive-
intel suites like Jungle Scout or Helium 10 for pre-launch homework.

A CrewAI crew that scopes the competition before you launch a physical
product. One agent pulls live retail listings from Amazon and Walmart, another
mines YouTube reviews and unboxings, an analyst compares pricing and
positioning, and a strategist writes the go-to-market angle. All retail and
video data comes through Scavio's unified Search API, so a single key covers
every source.

Prerequisites:
    pip install crewai crewai-scavio python-dotenv
    Env vars (in ../../.env): SCAVIO_API_KEY, OPENAI_API_KEY

Usage:
    python product-launch-crew.py "stainless steel insulated water bottle"
"""

import sys

from crewai import Agent, Crew, Process, Task
from crewai_scavio import (
    ScavioAmazonSearchTool,
    ScavioWalmartSearchTool,
    ScavioYouTubeSearchTool,
)
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "gpt-4o-mini"


def build_crew(product: str) -> Crew:
    amazon_tool = ScavioAmazonSearchTool()
    walmart_tool = ScavioWalmartSearchTool()
    youtube_tool = ScavioYouTubeSearchTool(sort_by="relevance")

    retail_scout = Agent(
        role="Retail Competitor Scout",
        goal=f"Find competing products for '{product}' on Amazon and Walmart.",
        backstory=(
            "A retail analyst who pulls live listings to map who you are up "
            "against on price, ratings, and feature claims."
        ),
        tools=[amazon_tool, walmart_tool],
        llm=MODEL,
        verbose=True,
    )

    review_scout = Agent(
        role="Review & Sentiment Scout",
        goal=f"Surface what YouTube reviewers say about '{product}' and rivals.",
        backstory=(
            "A researcher who watches the market through creator reviews and "
            "comparison videos to learn what buyers love and hate."
        ),
        tools=[youtube_tool],
        llm=MODEL,
        verbose=True,
    )

    analyst = Agent(
        role="Competitive Analyst",
        goal="Compare competitors on price, positioning, and reviewer sentiment.",
        backstory=(
            "A strategist who turns listing and review data into a clear picture "
            "of where the new product can win."
        ),
        llm=MODEL,
        verbose=True,
    )

    strategist = Agent(
        role="Launch Strategist",
        goal="Write a launch positioning and pricing recommendation.",
        backstory="A GTM lead who ships crisp, defensible launch plans.",
        llm=MODEL,
        verbose=True,
    )

    retail_task = Task(
        description=(
            f"Search Amazon and Walmart for '{product}'. List the top competing "
            "products with price, rating, and a notable selling point each."
        ),
        expected_output="A table-like list of competitor products from both retailers with price, rating, and selling point.",
        agent=retail_scout,
    )

    review_task = Task(
        description=(
            f"Search YouTube for reviews and comparisons of '{product}'. Summarize "
            "the recurring praise and complaints reviewers mention."
        ),
        expected_output="A summary of common praise and complaints from reviewer videos, with video titles.",
        agent=review_scout,
    )

    analysis_task = Task(
        description=(
            f"Using the retail and review findings for '{product}', compare "
            "competitors on price tiers and positioning, and identify the 3 most "
            "common buyer complaints to exploit."
        ),
        expected_output="A competitive analysis: price tiers, positioning map, and top exploitable complaints.",
        agent=analyst,
        context=[retail_task, review_task],
    )

    strategy_task = Task(
        description=(
            f"Write a launch plan for '{product}': recommended price band, the "
            "core positioning angle, 3 differentiating features to lead with, and "
            "2 marketing hooks drawn from competitor weaknesses."
        ),
        expected_output="A launch strategy brief in Markdown with price, positioning, features, and hooks.",
        agent=strategist,
        context=[analysis_task],
    )

    return Crew(
        agents=[retail_scout, review_scout, analyst, strategist],
        tasks=[retail_task, review_task, analysis_task, strategy_task],
        process=Process.sequential,
        verbose=True,
    )


def main() -> None:
    product = " ".join(sys.argv[1:]) or "stainless steel insulated water bottle"
    result = build_crew(product).kickoff()
    print("\n\n===== PRODUCT LAUNCH BRIEF =====\n")
    print(result)


if __name__ == "__main__":
    main()
