"""
PinterestContentPlanner: AI visual content strategy agent.

A free alternative to Tailwind, Pinacle, and Later for Pinterest content
research. Give it a niche or brand. It searches Pinterest pins, examines
top boards and profiles, checks URL save counts, and returns a content
plan: trending visual themes, optimal board structure, pin frequency,
and which blog URLs drive the most saves.

Built with LangChain create_agent, OpenAI tool calling, and custom
Scavio API tools for Pinterest data.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Get a free Scavio API key (50 free credits, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/pinterest-content-planner.py "minimalist home decor"
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
def scavio_pinterest_search(query: str) -> str:
    """Search Pinterest pins by keyword. Returns pins with title, description, images, destination link, video URL, board and pinner."""
    return _post("/api/v1/pinterest/search", {"query": query})


@tool
def scavio_pinterest_profile(username: str) -> str:
    """Get a Pinterest user profile: bio, website, follower/following counts, pin and board counts, merchant flag."""
    return _post("/api/v1/pinterest/profile", {"username": username})


@tool
def scavio_pinterest_user_boards(username: str) -> str:
    """List all public boards of a Pinterest user: name, description, pin count, follower count, cover image."""
    return _post("/api/v1/pinterest/user/boards", {"username": username})


@tool
def scavio_pinterest_url_stats(urls: list[str]) -> str:
    """Check how many times URLs have been saved to Pinterest (1-10 URLs per call). Returns per-URL save counts."""
    return _post("/api/v1/pinterest/url-stats", {"urls": urls})


SYSTEM_PROMPT = """You are PinterestContentPlanner. Given a niche or brand, \
produce a visual content strategy based on real Pinterest data.

## Workflow

1. SEARCH TRENDS
   Call scavio_pinterest_search with 2-3 keyword variants for the niche
   (e.g. "minimalist home decor", "minimalist interior", "scandinavian decor").
   Note the top pins: what visual themes recur, which destination URLs
   appear, which pinners dominate.

2. PROFILE ANALYSIS
   Pick 2-3 of the most active pinners from search results. Call
   scavio_pinterest_profile on each to gauge their audience size and
   activity level. Call scavio_pinterest_user_boards on the strongest
   one to see how they organize content.

3. URL PERFORMANCE (optional)
   If search results surface blog or product URLs, call
   scavio_pinterest_url_stats on up to 5 of those URLs to measure which
   domains earn the most saves.

4. SYNTHESIZE AND PLAN
   Return a content plan:

   NICHE: <niche>

   TRENDING VISUAL THEMES
   - <theme 1>: <what it looks like, why it works>
   - <theme 2>
   - <theme 3>

   TOP PINNERS IN THIS NICHE
   #1 @<username> -- <followers> followers, <pin_count> pins
      Board strategy: <how they organize boards>
   #2 ...

   RECOMMENDED BOARD STRUCTURE
   - <board 1 name>: <what goes in it>
   - <board 2 name>
   - <board 3 name>

   URL PERFORMANCE (if checked)
   - <domain>: <save_count> saves
   - ...

   CONTENT PLAN
   - Pin format: <what types of images/videos perform>
   - Frequency: <based on what top pinners do>
   - Keywords: <terms to use in pin descriptions>
   - Destination strategy: <where pins should link>

## Rules
- Only report data from actual Pinterest results. Never invent usernames,
  follower counts, save counts, or pin descriptions.
- Keep the final answer under 500 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [
        scavio_pinterest_search,
        scavio_pinterest_profile,
        scavio_pinterest_user_boards,
        scavio_pinterest_url_stats,
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "minimalist home decor"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
