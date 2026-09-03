"""
XTrendTracker: AI trending intelligence agent for X (Twitter).

A free alternative to Brandwatch and Talkwalker for tracking what is
trending on X. Give it a topic. It fetches the current trending board,
searches recent tweets, and reads engagement on top tweets. Returns a
trend report: volume signals, sentiment, key voices, and the
conversation arc.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
X API via custom tools.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/x-trend-tracker.py "AI agents"
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
HEADERS = lambda: {
    "Authorization": f"Bearer {os.environ.get('SCAVIO_API_KEY', '')}",
    "Content-Type": "application/json",
}


def _check_key() -> str | None:
    if not os.environ.get("SCAVIO_API_KEY"):
        return "Error: SCAVIO_API_KEY not set -- get a free key at https://dashboard.scavio.dev"
    return None


@tool
def scavio_x_trending(country: str = "UnitedStates") -> str:
    """Fetch X (Twitter) trending topics for a country."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/x/trending", headers=HEADERS(), json={"country": country}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


@tool
def scavio_x_search(query: str) -> str:
    """Search recent tweets on X by keyword. Returns tweets with engagement counts."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/x/search", headers=HEADERS(), json={"search": query, "search_type": "Top"}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_x_tweet_comments(tweet_id: str) -> str:
    """Fetch replies to a tweet to gauge conversation depth and sentiment."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/x/tweet/comments", headers=HEADERS(), json={"tweet_id": tweet_id}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


SYSTEM_PROMPT = """\
You are XTrendTracker. Given a topic, produce a trending intelligence \
report based on live X (Twitter) data.

## Workflow

1. TRENDING BOARD
   Call scavio_x_trending to get the current trending topics. Check
   whether the user's topic (or a close variant) appears. Note its
   rank and tweet volume if present.

2. SEARCH
   Call scavio_x_search with 2-3 query variants for the topic:
   - The topic itself
   - The topic + "2026" or a timely modifier
   - A related hashtag if obvious
   Combine and deduplicate results.

3. DEEP READ
   Pick the 1-2 highest-engagement tweets from search results (by
   likes + retweets). Call scavio_x_tweet_comments on each to
   understand the conversation depth and community sentiment.

4. REPORT
   Return:

   TOPIC: <topic>
   Trending: <yes (rank #N, ~volume) / not currently trending>

   TOP VOICES (from search results)
   - @<handle> (<followers>) -- "<tweet excerpt>" | <likes> likes, <retweets> RTs
   - ...

   CONVERSATION ARC
   <2-3 sentences: what is being said, what sub-topics are emerging,
   is the conversation growing or fading>

   SENTIMENT SIGNALS
   Positive: <% or description> | Negative: <% or description>
   <based on reply tone in the deep-read step>

   KEY TAKEAWAY
   <1-2 sentences: what this means for someone tracking this topic>

## Rules
- Only report data from tool results. Never invent handles or metrics.
- Keep under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_x_trending, scavio_x_search, scavio_x_tweet_comments]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(topic: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": f"Track this topic: {topic}"}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "AI agents"


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nTopic: {topic}\n{'-' * 60}")
    print(run(topic))
