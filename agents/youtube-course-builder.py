"""
YouTubeCourseBuilder: turn YouTube into a structured free course.

A free alternative to $50-$2,000 online courses. Give it a skill. It searches
YouTube across beginner-to-advanced angles, ranks the results by view count,
and assembles an ordered curriculum: modules from fundamentals to application,
each with a hand-picked video and why it belongs.

This recipe uses the Scavio Python SDK to search and trim, then an LLM to plan,
because raw YouTube payloads are large -- fetch, keep only the useful fields,
then reason. A clean pattern for any high-volume source.

Prerequisites:
  pip install scavio langchain-openai python-dotenv
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/youtube-course-builder.py "learn rust programming"
"""

import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from scavio import ScavioClient

load_dotenv(override=True)


def gather(skill: str) -> list:
    client = ScavioClient()
    angles = [
        f"{skill} for beginners",
        f"{skill} full course",
        f"{skill} projects",
    ]
    seen, videos = set(), []
    for angle in angles:
        results = (
            client.youtube.search(angle, sort_by="view_count").get("data") or {}
        ).get("results") or []
        for r in results[:6]:
            vid = r.get("video_id")
            if not vid or vid in seen:
                continue
            seen.add(vid)
            views = r.get("view_count")
            videos.append(
                {
                    "id": vid,
                    "title": r.get("title") or "",
                    "channel": (r.get("channel") or {}).get("name") or "",
                    "views": f"{views:,}" if isinstance(views, int) else "",
                    "length": r.get("duration_text") or "",
                    "url": r.get("url") or f"https://youtube.com/watch?v={vid}",
                }
            )
    return videos


PROMPT = """You are YouTubeCourseBuilder. From the YouTube videos below (real
titles, channels, view counts, lengths, and URLs), build a free, ordered
curriculum for learning "{skill}".

Output:
  # Course: {skill}
  ## Module N -- <theme>
  <title> -- <channel>  (<views>, <length>)
  <url>
  Why: <one line>

Use 4-6 modules, ordered fundamentals -> application. Prefer substantial,
high-view videos; skip clickbait and very short clips for core modules. Use
only the videos provided -- never invent titles, channels, or URLs. End with a
one-line suggested pace. Keep it under 450 words.

VIDEOS:
{videos}
"""


def run(skill: str) -> str:
    import json

    videos = gather(skill)
    llm = ChatOpenAI(model="gpt-5.5", temperature=0)
    prompt = PROMPT.format(skill=skill, videos=json.dumps(videos, indent=1))
    return llm.invoke(prompt).content


if __name__ == "__main__":
    skill = " ".join(sys.argv[1:]) or "learn rust programming"
    print(f"\nSkill: {skill}\n{'-' * 60}")
    print(run(skill))
