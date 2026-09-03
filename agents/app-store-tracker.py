"""
AppStoreTracker: AI app store optimization and competitor tracking agent.

A free alternative to Sensor Tower, data.ai, and AppTweak for ASO
research. Give it an app category or keyword. It searches both the Apple
App Store and Google Play, examines top apps, reads reviews, and returns
an ASO intelligence brief.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
real-time search API (App Store + Google Play endpoints).

Prerequisites:
  pip install langchain langchain-openai python-dotenv requests

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/app-store-tracker.py "habit tracker"
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


def _post(path: str, body: dict) -> str:
    key = os.environ.get("SCAVIO_API_KEY")
    if not key:
        return "Error: SCAVIO_API_KEY not set -- get a free key at https://dashboard.scavio.dev"
    try:
        resp = requests.post(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=body,
            timeout=60,
        )
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_appstore_search(query: str) -> str:
    """Search the Apple App Store for apps matching a keyword."""
    return _post("/api/v1/appstore/search", {"term": query})


@tool
def scavio_appstore_app(app_id: str) -> str:
    """Get full details for an App Store app by its numeric app id."""
    return _post("/api/v1/appstore/app", {"app_id": app_id})


@tool
def scavio_appstore_reviews(app_id: str) -> str:
    """Get App Store reviews for an app by its numeric app id."""
    return _post("/api/v1/appstore/reviews", {"app_id": app_id})


@tool
def scavio_googleplay_search(query: str) -> str:
    """Search Google Play for apps matching a keyword."""
    return _post("/api/v1/googleplay/search", {"query": query})


@tool
def scavio_googleplay_app(app_id: str) -> str:
    """Get full details for a Google Play app by its package name."""
    return _post("/api/v1/googleplay/app", {"app_id": app_id})


SYSTEM_PROMPT = """\
You are AppStoreTracker. Given an app category or keyword, produce an ASO
intelligence brief covering both iOS and Android.

## Workflow

1. SEARCH BOTH STORES
   Call scavio_appstore_search and scavio_googleplay_search with the
   keyword. Note the top 5-8 apps on each platform: name, rating,
   review count, price/IAP model.

2. DEEP-READ TOP APPS
   Pick 2-3 top-ranked apps. Call scavio_appstore_app or
   scavio_googleplay_app for details: description, screenshots hint,
   version history, size, category.

3. READ REVIEWS
   Call scavio_appstore_reviews on 1-2 of the top iOS apps. Note the
   most recent praise and complaints.

4. SYNTHESIZE AND ANSWER
   Return a brief with these sections:

   KEYWORD COMPETITION
   - Number of apps found on each platform for this keyword
   - Top 5 apps by rank with their rating and review count

   RATING DISTRIBUTION
   - Average rating across the top results on each platform
   - Any app with < 4.0 that still ranks high (opportunity signal)

   COMMON COMPLAINTS (from reviews)
   - 3-5 recurring negative themes across top apps

   FEATURE GAPS
   - Based on complaints and descriptions, what features are users
     asking for that no top app delivers well?

   ASO SIGNAL
   - One paragraph: how crowded is this keyword, and where is the
     opening for a new entrant?

## Rules
- Only cite app names, ratings, and review quotes from API responses.
- If a store returns fewer apps, report the actual count.
- Keep the final answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [
        scavio_appstore_search,
        scavio_appstore_app,
        scavio_appstore_reviews,
        scavio_googleplay_search,
        scavio_googleplay_app,
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(keyword: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": keyword}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "habit tracker"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nKeyword: {brief}\n{'-' * 60}")
    print(run(brief))
