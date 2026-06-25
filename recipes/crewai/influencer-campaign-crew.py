"""
Influencer-campaign crew: a free alternative to paid creator-discovery
platforms like Upfluence or HypeAuditor for building a first shortlist.

A CrewAI crew that turns a campaign brief into a shortlist of TikTok and
Instagram creators to approach. One scout searches TikTok creators and trending
videos for the niche, another searches Instagram creators and hashtags, an
analyst ranks the candidates, and a planner writes the outreach shortlist. All
social discovery runs through Scavio's unified Search API with a single key.

Prerequisites:
    pip install crewai crewai-scavio python-dotenv
    Env vars (in ../../.env): SCAVIO_API_KEY, OPENAI_API_KEY

Usage:
    python influencer-campaign-crew.py "sustainable activewear for runners"
"""

import sys

from crewai import Agent, Crew, Process, Task
from crewai_scavio import (
    ScavioInstagramSearchHashtagsTool,
    ScavioInstagramSearchUsersTool,
    ScavioTikTokSearchUsersTool,
    ScavioTikTokSearchVideosTool,
)
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "gpt-4o-mini"


def build_crew(brief: str) -> Crew:
    # Social search payloads are large; cap results so several calls fit
    # comfortably inside the model's context window.
    tiktok_users_tool = ScavioTikTokSearchUsersTool(max_results=3)
    tiktok_videos_tool = ScavioTikTokSearchVideosTool(max_results=3)
    instagram_users_tool = ScavioInstagramSearchUsersTool(max_results=3)
    instagram_hashtags_tool = ScavioInstagramSearchHashtagsTool(max_results=3)

    tiktok_scout = Agent(
        role="TikTok Creator Scout",
        goal=f"Find TikTok creators and trending videos relevant to: {brief}.",
        backstory=(
            "A social scout who searches TikTok for creators and the videos that "
            "are actually getting traction in a niche."
        ),
        tools=[tiktok_users_tool, tiktok_videos_tool],
        llm=MODEL,
        verbose=True,
    )

    instagram_scout = Agent(
        role="Instagram Creator Scout",
        goal=f"Find Instagram creators and active hashtags relevant to: {brief}.",
        backstory=(
            "A scout who maps Instagram creators and the hashtags their audience "
            "follows to gauge reach and relevance."
        ),
        tools=[instagram_users_tool, instagram_hashtags_tool],
        llm=MODEL,
        verbose=True,
    )

    analyst = Agent(
        role="Influencer Analyst",
        goal="Rank candidate creators on relevance and apparent reach.",
        backstory=(
            "An influencer-marketing analyst who weighs niche fit, audience "
            "signals, and content consistency to rank creators."
        ),
        llm=MODEL,
        verbose=True,
    )

    planner = Agent(
        role="Campaign Planner",
        goal="Produce a creator shortlist with outreach angles.",
        backstory="A campaign manager who turns a ranked list into an actionable outreach plan.",
        llm=MODEL,
        verbose=True,
    )

    tiktok_task = Task(
        description=(
            f"Search TikTok for creators and trending videos matching the brief: "
            f"'{brief}'. Make at most one creator search and one video search "
            "using a single focused keyword. From the results, list up to 5 "
            "candidate creators with handles and a short note on the content "
            "they make. Do not repeat searches."
        ),
        expected_output="A short list of TikTok creators (handles + content notes) and a few example trending videos.",
        agent=tiktok_scout,
    )

    instagram_task = Task(
        description=(
            f"Search Instagram for creators and relevant hashtags for the brief: "
            f"'{brief}'. Make at most one user search and one hashtag search "
            "using a single focused keyword. List up to 5 candidate creators "
            "with handles plus the hashtags their niche uses. Do not repeat "
            "searches."
        ),
        expected_output="A short list of Instagram creators (handles + notes) and relevant active hashtags.",
        agent=instagram_scout,
    )

    analysis_task = Task(
        description=(
            f"From the TikTok and Instagram candidates for '{brief}', rank the top "
            "8 creators across both platforms. For each, note platform, handle, "
            "why they fit, and a rough sense of reach."
        ),
        expected_output="A ranked top-8 creator list with platform, handle, fit rationale, and reach signal.",
        agent=analyst,
        context=[tiktok_task, instagram_task],
    )

    plan_task = Task(
        description=(
            f"Write the final influencer shortlist for the campaign '{brief}'. "
            "For each shortlisted creator include platform, handle, why they fit, "
            "and a one-line outreach angle."
        ),
        expected_output="A creator shortlist in Markdown with outreach angles.",
        agent=planner,
        context=[analysis_task],
    )

    return Crew(
        agents=[tiktok_scout, instagram_scout, analyst, planner],
        tasks=[tiktok_task, instagram_task, analysis_task, plan_task],
        process=Process.sequential,
        verbose=True,
    )


def main() -> None:
    brief = " ".join(sys.argv[1:]) or "sustainable activewear for runners"
    result = build_crew(brief).kickoff()
    print("\n\n===== INFLUENCER SHORTLIST =====\n")
    print(result)


if __name__ == "__main__":
    main()
