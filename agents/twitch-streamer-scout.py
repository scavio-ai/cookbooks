"""
TwitchStreamerScout: AI gaming/streaming sponsorship scouting agent.

A free alternative to SullyGnome, TwitchTracker, and Stream Hatchet
for finding Twitch streamers to sponsor. Give it a game or category.
It profiles relevant streamers, checks their video libraries and
schedules, and returns a scouting report: streamer tier, streaming
consistency, content focus, and sponsorship fit.

Built with LangChain create_agent, OpenAI tool calling, and custom
Scavio API tools for Twitch data.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Get a free Scavio API key (50 free credits, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/twitch-streamer-scout.py "Valorant streamers for a \
gaming headset brand, 5k-100k followers"
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

API_BASE = "https://api.scavio.dev"


def _headers():
    key = os.environ.get("SCAVIO_API_KEY", "")
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def _post(path: str, body: dict) -> str:
    if not os.environ.get("SCAVIO_API_KEY"):
        return "Error: SCAVIO_API_KEY not set -- get a free key at https://dashboard.scavio.dev"
    try:
        resp = requests.post(f"{API_BASE}{path}", headers=_headers(), json=body, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_twitch_profile(handle: str) -> str:
    """Get a Twitch channel profile: display name, follower count, broadcaster type, live status, current stream game and title, profile image."""
    return _post("/api/v1/twitch/profile", {"handle": handle})


@tool
def scavio_twitch_user_videos(handle: str) -> str:
    """Get a Twitch channel's recent VODs, highlights, and uploads: title, duration, view count, game, publish date."""
    return _post("/api/v1/twitch/user/videos", {"handle": handle})


@tool
def scavio_twitch_user_schedule(handle: str) -> str:
    """Get a Twitch channel's stream schedule: recurring segments with title, game, day, and time."""
    return _post("/api/v1/twitch/user/schedule", {"handle": handle})


SYSTEM_PROMPT = """You are TwitchStreamerScout. Given a game/category and a \
sponsorship brief, find and evaluate Twitch streamers for brand campaigns.

## Parse the brief

Extract:
- The game or category (e.g. "Valorant", "Just Chatting", "retro games")
- Any follower range constraints
- The brand or product type if mentioned

## Workflow

1. IDENTIFY CANDIDATES
   You will receive streamer usernames as part of the brief, or you should
   suggest well-known streamers for that game/category. Call
   scavio_twitch_profile on 4-6 candidate usernames to get their
   follower counts, live status, and current game.

2. EVALUATE CONTENT
   For the top 3-4 candidates (by follower fit and game relevance), call
   scavio_twitch_user_videos to see recent VOD titles, games played,
   stream durations, and view counts. This reveals content consistency
   and audience engagement.

3. CHECK SCHEDULE
   Call scavio_twitch_user_schedule on the top candidates. A published
   schedule signals professionalism and predictable sponsorship windows.

4. SCOUT REPORT
   Return a ranked scouting report:

   CATEGORY: <game/category>
   Streamers evaluated: <N>

   #1 <display_name> (@<username>)
   Followers: <count> | Tier: <micro/mid/macro>
   Live now: <yes/no> | Current game: <game>
   Schedule: <has one / none published>
   Content: <recent games, average VOD duration, view counts>
   Fit: <one line on why this streamer fits the brief>

   #2 ...
   #3 ...

   RECOMMENDATION
   <one paragraph: which streamer to approach first and why,
    suggested sponsorship format (overlay, dedicated stream,
    product placement), and timing based on schedule>

## Rules
- Only report data from actual Twitch API results. Never invent
  usernames, follower counts, view counts, or schedule data.
- If a streamer has no schedule, note it as a signal (less professional,
  harder to plan sponsorship windows).
- Keep the final answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_twitch_profile, scavio_twitch_user_videos, scavio_twitch_user_schedule]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = (
    "Valorant streamers for a gaming headset brand launch. "
    "Looking for mid-tier streamers (5k-100k followers) who stream "
    "regularly and have an engaged audience. Check: shroud, tarik, "
    "tenz, sinatraa, s0m"
)


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
