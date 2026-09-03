"""
ThreadsGrowthFinder: AI Threads platform growth opportunity agent.

Finds growth opportunities on Meta's Threads by analyzing niche activity,
top voices, engagement patterns, and content themes that drive replies.
Give it a niche. It searches Threads users, examines profiles and posts,
and returns a growth report with actionable insights.

Built with LangChain create_agent, OpenAI tool calling, and custom
Scavio API tools for Threads data.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Get a free Scavio API key (50 free credits, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/threads-growth-finder.py "AI and machine learning"
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
def scavio_threads_search_users(query: str) -> str:
    """Search Threads profiles by name or handle. Returns usernames, follower counts, bios, and verified flags."""
    return _post("/api/v1/threads/search/users", {"query": query})


@tool
def scavio_threads_profile(username: str) -> str:
    """Get a Threads user profile: follower/following counts, bio, verified status, and link."""
    return _post("/api/v1/threads/profile", {"username": username})


@tool
def scavio_threads_user_posts(username: str) -> str:
    """Get a Threads user's recent posts: text, like count, reply count, repost count, and timestamp."""
    return _post("/api/v1/threads/user/posts", {"username": username})


SYSTEM_PROMPT = """You are ThreadsGrowthFinder. Given a niche, find growth \
opportunities on Meta's Threads platform using real data.

## Workflow

1. DISCOVER
   Call scavio_threads_search_users with 2-3 keyword variants for the
   niche (e.g. "AI", "machine learning", "artificial intelligence").
   Note all returned profiles: username, follower count, bio, verified.
   Deduplicate across searches.

2. PROFILE DEEP DIVE
   For the 3-4 most relevant accounts (by follower count and bio fit),
   call scavio_threads_profile for full profile data, then
   scavio_threads_user_posts to see recent content.

3. ANALYZE
   From the posts, identify:
   - Engagement patterns: which post types (questions, opinions, threads,
     links) get the most likes and replies
   - Posting frequency: how often the top accounts post
   - Content themes: recurring topics that resonate
   - Reply-to-like ratio: higher reply ratios signal discussion-worthy
     content (not just passive consumption)

4. REPORT
   Return a growth report:

   NICHE: <niche> on Threads

   TOP VOICES
   #1 @<username> -- <followers> followers (verified: yes/no)
   Bio: <bio summary>
   Posting pace: <posts per week estimate>
   Top-performing post: <brief description + like/reply counts>

   #2 ...
   #3 ...

   ENGAGEMENT PATTERNS
   - What drives replies: <theme/format>
   - What drives likes only: <theme/format>
   - Average engagement: <likes/replies per post across the set>

   CONTENT THEMES THAT WORK
   - <theme 1>
   - <theme 2>
   - <theme 3>

   GROWTH PLAYBOOK
   <one paragraph: how a new account in this niche should position
    itself, what to post, when, and who to engage with first>

## Rules
- Only report data from actual Threads results. Never invent usernames,
  follower counts, post text, or engagement metrics.
- If the niche is too narrow and search returns few results, say so and
  suggest adjacent queries the user could try.
- Keep the final answer under 450 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_threads_search_users, scavio_threads_profile, scavio_threads_user_posts]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "AI and machine learning"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
