"""
FacebookBrandMonitor: AI brand monitoring agent for Facebook pages.

A free alternative to Brand24 and Mention for tracking brand presence
on Facebook. Give it a brand's Facebook page URL. It pulls the page
profile, recent posts, and hashtag mentions, then analyzes engagement
patterns, top-performing content themes, and reputation signals.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
Facebook API via custom tools.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/facebook-brand-monitor.py "https://www.facebook.com/nike"
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
def scavio_facebook_profile(url: str) -> str:
    """Fetch a Facebook page profile: name, category, followers, likes, bio, website, contact info."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/facebook/profile", headers=HEADERS(), json={"url": url}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


@tool
def scavio_facebook_posts(url: str) -> str:
    """Fetch a Facebook page's recent posts: text, reactions, comments, shares, media."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/facebook/profile/posts", headers=HEADERS(), json={"url": url}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_facebook_hashtag(tag: str) -> str:
    """Fetch top public posts for a Facebook hashtag: author, text, reactions, media."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/facebook/hashtag", headers=HEADERS(), json={"tag": tag}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


SYSTEM_PROMPT = """\
You are FacebookBrandMonitor. Given a brand's Facebook page URL, produce \
a brand-health monitoring report.

## Workflow

1. PROFILE
   Call scavio_facebook_profile with the page URL. Extract: name,
   category, follower count, likes, verified status, bio and website.

2. RECENT POSTS
   Call scavio_facebook_posts with the same URL. For each post, note
   the text, total reactions, reaction breakdown by type, comment count,
   share count, and media type.

3. HASHTAG PULSE
   From the brand name, derive 1-2 hashtag variants (e.g. the brand
   name itself, a known campaign tag). Call scavio_facebook_hashtag on
   each. Note whether third-party accounts mention the brand positively,
   negatively, or neutrally.

4. ANALYZE AND REPORT
   Return a structured monitoring report:

   BRAND: <name> (<category>)
   Followers: <N> | Likes: <N> | Verified: <yes/no>

   ENGAGEMENT SNAPSHOT (last ~10 posts)
   Avg reactions/post: <N>
   Avg comments/post: <N>
   Avg shares/post: <N>
   Dominant reaction type: <like/love/haha/wow/sad/angry>

   TOP PERFORMING CONTENT
   #1: "<post excerpt>" -- <reactions> reactions, <shares> shares
   #2: ...
   Theme: <what content type or topic drives engagement>

   HASHTAG MENTIONS
   #<tag>: <N posts found> -- sentiment: <positive/mixed/negative>

   REPUTATION SIGNALS
   - <any angry-reaction spikes, negative comments, PR issues>
   - <or: no red flags detected>

   RECOMMENDATIONS
   - <1-2 actionable suggestions based on data>

## Rules
- Only report data from tool results. Never invent metrics.
- Keep under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_facebook_profile, scavio_facebook_posts, scavio_facebook_hashtag]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(page_url: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": f"Monitor this brand: {page_url}"}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "https://www.facebook.com/nike"


if __name__ == "__main__":
    page_url = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nPage: {page_url}\n{'-' * 60}")
    print(run(page_url))
