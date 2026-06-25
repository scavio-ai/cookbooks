"""
Market-research crew: a free, self-hosted alternative to paid research
copilots like Crayon or AlphaSense for quick niche briefs.

A 3-agent CrewAI crew (researcher, analyst, writer) that turns a product or
niche into a structured market-research brief. The researcher pulls live
signal from Google (via Scavio's unified Search API) and Reddit discussions,
the analyst distills demand, competitors, and gaps, and the writer ships a
clean brief. All web data comes from the Scavio Search API, so there is no
scraping, proxies, or per-source API keys to manage.

Prerequisites:
    pip install crewai crewai-scavio python-dotenv
    Env vars (in ../../.env): SCAVIO_API_KEY, OPENAI_API_KEY

Usage:
    python market-research-crew.py "AI note-taking apps for students"
"""

import sys

from crewai import Agent, Crew, Process, Task
from crewai_scavio import ScavioRedditSearchTool, ScavioSearchTool
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "gpt-4o-mini"


def build_crew(niche: str) -> Crew:
    search_tool = ScavioSearchTool()
    reddit_tool = ScavioRedditSearchTool(sort="relevance")

    researcher = Agent(
        role="Market Research Analyst",
        goal=f"Gather live market signal on '{niche}' from the web and Reddit.",
        backstory=(
            "A meticulous researcher who only trusts current, sourced data. "
            "You search Google for market context and Reddit for unfiltered "
            "user sentiment, then hand over raw findings with sources."
        ),
        tools=[search_tool, reddit_tool],
        llm=MODEL,
        verbose=True,
    )

    analyst = Agent(
        role="Strategy Analyst",
        goal="Turn raw research into demand, competitor, and gap insights.",
        backstory=(
            "A sharp strategist who reads between the lines of search results "
            "and community chatter to find what the market actually wants and "
            "where incumbents fall short."
        ),
        llm=MODEL,
        verbose=True,
    )

    writer = Agent(
        role="Brief Writer",
        goal="Write a concise, decision-ready market-research brief.",
        backstory=(
            "A clear writer who packages analysis into a brief an operator can "
            "act on in five minutes."
        ),
        llm=MODEL,
        verbose=True,
    )

    research_task = Task(
        description=(
            f"Research the market for '{niche}'. Use the search tool for market "
            "size, trends, and notable players, and the Reddit tool for what "
            "real users praise and complain about. Collect at least 6 concrete "
            "findings with sources."
        ),
        expected_output="A bulleted list of sourced findings covering trends, players, and user sentiment.",
        agent=researcher,
    )

    analysis_task = Task(
        description=(
            f"Analyze the findings on '{niche}'. Identify demand drivers, the top "
            "competitors and their positioning, and 3 unmet needs or gaps."
        ),
        expected_output="Structured analysis: demand drivers, competitor map, and a list of market gaps.",
        agent=analyst,
        context=[research_task],
    )

    writing_task = Task(
        description=(
            f"Write a market-research brief on '{niche}' using the analysis. "
            "Include: Overview, Demand & Trends, Competitive Landscape, "
            "Opportunities/Gaps, and a one-line Recommendation."
        ),
        expected_output="A clean, sectioned market-research brief in Markdown.",
        agent=writer,
        context=[analysis_task],
    )

    return Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )


def main() -> None:
    niche = " ".join(sys.argv[1:]) or "AI note-taking apps for students"
    result = build_crew(niche).kickoff()
    print("\n\n===== MARKET RESEARCH BRIEF =====\n")
    print(result)


if __name__ == "__main__":
    main()
