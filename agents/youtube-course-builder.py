"""
YouTubeCourseBuilder: turn YouTube into a structured free course.

A free alternative to $50-$2,000 online courses. Give it a skill. It searches
YouTube for the best tutorials, ranks them by real engagement (views, likes,
comments via metadata), and assembles an ordered curriculum: modules from
beginner to advanced, each with a hand-picked video and why it belongs.

Built with LangChain create_agent, OpenAI tool calling, and langchain-scavio
YouTube tools.

Prerequisites:
  pip install langchain langchain-openai "langchain-scavio>=2.9" python-dotenv
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/youtube-course-builder.py "learn rust programming"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioYouTubeMetadata, ScavioYouTubeSearch

load_dotenv(override=True)


SYSTEM_PROMPT = """You are YouTubeCourseBuilder. Given a skill, build a free,
ordered video curriculum.

## Workflow

1. Generate 3-4 search angles spanning beginner -> intermediate -> advanced
   (e.g. "<skill> for beginners", "<skill> full course", "<skill> projects").
2. Call ScavioYouTubeSearch for each angle. Collect candidate videos.
3. For the most promising 5-8 videos, call ScavioYouTubeMetadata to get real
   view_count, like_count, and duration. Prefer high-engagement, substantial
   videos; drop clickbait and very short clips for core modules.
4. ANSWER as a curriculum:

   # Course: <skill>

   ## Module 1 -- <theme>
   <video title> -- <channel>  (<views> views, <duration>)
   https://youtube.com/watch?v=<id>
   Why: <one line>

   ...3-6 modules, ordered from fundamentals to application.

   End with a one-line "suggested pace".

## Rules
- Only use videos returned by the tools, with their real IDs and metrics.
- Never invent titles, channels, view counts, or video IDs.
- Keep the answer under 450 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [ScavioYouTubeSearch(max_results=8), ScavioYouTubeMetadata()]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(skill: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": skill}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    skill = " ".join(sys.argv[1:]) or "learn rust programming"
    print(f"\nSkill: {skill}\n{'-' * 60}")
    print(run(skill))
