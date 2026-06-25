"""
SEO content crew: a free alternative to paid SEO content tools like Surfer
or Frase for turning a seed keyword into a content plan.

A CrewAI crew that mines live Google results, related searches, and
"people also ask" questions for a seed keyword (via Scavio's unified Search
API), clusters the intent, and writes an SEO content plan with an outline and
target subtopics. No keyword-tool subscription required -- one Scavio key
covers the SERP data.

Prerequisites:
    pip install crewai crewai-scavio python-dotenv
    Env vars (in ../../.env): SCAVIO_API_KEY, OPENAI_API_KEY

Usage:
    python seo-content-crew.py "home espresso machines"
"""

import sys

from crewai import Agent, Crew, Process, Task
from crewai_scavio import ScavioSearchTool
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "gpt-4o-mini"


def build_crew(keyword: str) -> Crew:
    search_tool = ScavioSearchTool()

    serp_researcher = Agent(
        role="SERP Researcher",
        goal=f"Map the search landscape for the seed keyword '{keyword}'.",
        backstory=(
            "An SEO researcher who reads the live SERP -- top ranking pages, "
            "related searches, and people-also-ask questions -- to understand "
            "what Google rewards for a keyword."
        ),
        tools=[search_tool],
        llm=MODEL,
        verbose=True,
    )

    strategist = Agent(
        role="Content Strategist",
        goal="Cluster keywords by search intent and find content gaps.",
        backstory=(
            "A content strategist who groups queries by intent and spots angles "
            "the current top results miss."
        ),
        llm=MODEL,
        verbose=True,
    )

    planner = Agent(
        role="Content Planner",
        goal="Write an SEO content plan with a full outline.",
        backstory="An editor who turns intent research into a brief a writer can execute.",
        llm=MODEL,
        verbose=True,
    )

    research_task = Task(
        description=(
            f"Research the SERP for '{keyword}'. Run the seed query plus 2-3 "
            "variations. Collect the themes of top-ranking pages, related "
            "searches, and any people-also-ask questions you find."
        ),
        expected_output="A list of top-ranking page themes, related searches, and PAA-style questions with sources.",
        agent=serp_researcher,
    )

    strategy_task = Task(
        description=(
            f"From the SERP research on '{keyword}', cluster the queries and "
            "questions into 3-5 intent groups (informational, commercial, etc.) "
            "and name 3 content gaps the top results do not cover well."
        ),
        expected_output="Intent clusters with their queries, plus a list of content gaps.",
        agent=strategist,
        context=[research_task],
    )

    plan_task = Task(
        description=(
            f"Write an SEO content plan for '{keyword}': a target title, primary "
            "and secondary keywords, an H2/H3 outline covering the intent "
            "clusters, an FAQ section built from the PAA questions, and a short "
            "note on the angle that beats the current top results."
        ),
        expected_output="A complete SEO content plan in Markdown: title, keywords, outline, FAQ, and differentiation note.",
        agent=planner,
        context=[strategy_task],
    )

    return Crew(
        agents=[serp_researcher, strategist, planner],
        tasks=[research_task, strategy_task, plan_task],
        process=Process.sequential,
        verbose=True,
    )


def main() -> None:
    keyword = " ".join(sys.argv[1:]) or "home espresso machines"
    result = build_crew(keyword).kickoff()
    print("\n\n===== SEO CONTENT PLAN =====\n")
    print(result)


if __name__ == "__main__":
    main()
