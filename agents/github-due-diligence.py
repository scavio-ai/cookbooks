"""
GitHubDD: AI due-diligence agent for GitHub repositories.

A free alternative to paid repo-analytics dashboards for investors,
acquirers, and engineering leaders. Give it a repo. It pulls the composite
dossier, top issues, and lead-maintainer velocity, then synthesizes a
structured due-diligence brief: project health, contributor concentration
risk, issue backlog, release cadence, and red flags.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
GitHub API via custom tools.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/github-due-diligence.py "facebook/react"
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
def scavio_github_dossier(url: str) -> str:
    """Fetch a composite GitHub repo dossier: metadata, README excerpt, releases, top issues, language breakdown, contributors and weekly activity."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/github/repo/dossier", headers=HEADERS(), json={"url": url}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_github_top_issues(url: str) -> str:
    """Fetch a repo's most-reacted open issues, ranked by community demand."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/github/repo/top-issues", headers=HEADERS(), json={"url": url, "per_page": 10}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


@tool
def scavio_github_user_velocity(handle: str) -> str:
    """Fetch a GitHub user's public-activity velocity: event counts, active days, events/week over the last 90 days."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/github/user/profile-velocity", headers=HEADERS(), json={"handle": handle}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:4000]


SYSTEM_PROMPT = """\
You are GitHubDD. Given a GitHub repository, produce a structured \
due-diligence brief for an investor or acquirer.

## Workflow

1. DOSSIER
   Call scavio_github_dossier with the repo URL. Extract: stars, forks,
   open issues, license, language breakdown, top contributors, latest
   releases, weekly commit activity, and the README excerpt.

2. TOP ISSUES
   Call scavio_github_top_issues on the same repo. Identify the most
   community-demanded features or longest-standing bugs.

3. LEAD MAINTAINER VELOCITY
   From the dossier's top contributors, pick the #1 contributor by
   commits. Call scavio_github_user_velocity on that handle. Assess
   whether the project depends on a single maintainer.

4. SYNTHESIZE
   Return a structured brief:

   PROJECT: <owner/repo>
   HEALTH SCORE: <1-10> (<one-line rationale>)

   Stars / Forks: <N> / <N>
   License: <license>
   Languages: <top 3 with %>

   RELEASE CADENCE
   Last release: <tag> (<date>)
   Recent release frequency: <e.g. monthly / quarterly / stalled>

   CONTRIBUTOR RISK
   Top contributor: @<handle> -- <% of recent commits>
   Bus factor assessment: <low / medium / high risk>
   Lead maintainer velocity: <events/week, active days in 90d>

   ISSUE BACKLOG
   Open issues: <N>
   Top community demands:
   - <issue title> (<reactions> reactions)
   - ...

   RED FLAGS
   - <anything concerning: stale releases, single-maintainer, license,
     declining activity, mass unresolved issues>

   SUMMARY: <2-3 sentence investment thesis or caution>

## Rules
- Only report data from tool results. Never invent stats.
- Keep the brief under 500 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_github_dossier, scavio_github_top_issues, scavio_github_user_velocity]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(repo: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": f"Run due diligence on: {repo}"}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "facebook/react"


if __name__ == "__main__":
    repo = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nRepo: {repo}\n{'-' * 60}")
    print(run(repo))
