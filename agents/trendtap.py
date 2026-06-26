"""
TrendTap: AI content idea generator using YouTube, Reddit, and Google trends.

A free alternative to VidIQ, TubeBuddy, and Exploding Topics for content
research. Give it a niche or topic and it finds trending YouTube videos,
active Reddit discussions, and Google People Also Ask questions, then
outputs ranked content ideas with data from each source. Built for
YouTubers, bloggers, newsletter writers, and social media managers.

Built with LangChain create_agent, OpenAI tool calling, and langchain-scavio
YouTube + Reddit + Google search tools.

Prerequisites:
  pip install langchain langchain-openai langchain-scavio python-dotenv

  Get a free Scavio API key (50 free credits, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/trendtap.py "home espresso"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import (
    ScavioRedditSearch,
    ScavioSearch,
    ScavioYouTubeMetadata,
    ScavioYouTubeSearch,
)

load_dotenv(override=True)


SYSTEM_PROMPT = """You are TrendTap, a content research analyst that finds \
trending topics and content gaps for YouTubers, bloggers, and social media \
managers.

IMPORTANT: Call only ONE tool per step. The API rate-limits concurrent
requests. Never call two search tools in the same turn.

## Workflow

1. YOUTUBE LANDSCAPE
   Call ScavioYouTubeSearch for the user's topic. Analyze the top 10
   results for patterns: which angles get the most views? Are there
   recent uploads outperforming older ones (signal of rising interest)?
   Call ScavioYouTubeMetadata on the top 2-3 videos by view count to
   get detailed stats (likes, comments, publish date).

2. REDDIT DEMAND
   Call ScavioRedditSearch for the topic with sort="new". Look for:
   - Questions people are asking (unanswered = content opportunity)
   - Product recommendations threads (affiliate content angles)
   - Debates or controversies (opinion content angles)
   - "How to" or "beginner" posts (tutorial content angles)

3. GOOGLE SIGNALS
   Call ScavioSearch for "<topic> 2026" and "<topic> guide". Extract:
   - People Also Ask questions (direct content titles)
   - Related searches (subtopic ideas)
   - What type of content currently ranks (video, listicle, guide)

4. OUTPUT
   Return a ranked list of content ideas:

   CONTENT IDEAS: "<topic>"
   ============================================================

   #1  <Content title idea>
       Format: <YouTube video / Blog post / Thread / Short>
       Why now: <what data point signals demand>
       YouTube proof: "<video title>" -- <views> views in <age>
       Reddit proof: r/<sub> -- "<thread title>" -- <N> comments
       Google proof: PAA: "<people also ask question>"
       Difficulty: <Low / Medium / High> (based on existing competition)

   #2  <Content title idea>
       ...

   Repeat for up to 7 ideas.

   QUICK WINS
   List 3 People Also Ask questions from Google that have no good
   YouTube video answering them yet. These are low-competition
   opportunities.

   AVOID
   List 1-2 angles that look saturated (too many high-view videos,
   dominant Reddit threads already answered) -- creating content here
   would be wasted effort.

## Rules
- Never invent video titles, view counts, subreddit names, or PAA
  questions. Only use tool output.
- Rank ideas by a combination of demand (views, comments, search
  volume signals) and competition (fewer existing videos = better).
- If the topic is too broad, narrow it to 2-3 subtopics and research
  each.
- Keep the final answer under 500 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    tools = [
        ScavioYouTubeSearch(max_results=5),
        ScavioYouTubeMetadata(),
        ScavioRedditSearch(max_results=5),
        ScavioSearch(max_results=5),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(query: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


DEFAULT_QUERY = "home espresso"


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    print(f"\nQuery: {query}\n{'-' * 60}")
    print(run(query))
