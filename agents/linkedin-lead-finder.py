"""
LinkedInLeadFinder: AI B2B lead generation agent for LinkedIn.

A free alternative to Apollo, ZoomInfo, and LinkedIn Sales Navigator
for sourcing company intelligence and engagement opportunities. Give
it a target company name and optional role keywords. It pulls the
company profile, recent posts, and open roles, then returns a brief
with company intel, growth signals, and engagement angles.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
LinkedIn API via custom tools.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/linkedin-lead-finder.py "Microsoft, looking for AI \
engineering leaders to pitch our developer tools"
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
def scavio_linkedin_company(company: str) -> str:
    """Fetch a LinkedIn company profile: description, industry, size, locations, featured employees."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/linkedin/company", headers=HEADERS(), json={"company": company}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:6000]


@tool
def scavio_linkedin_company_posts(company: str) -> str:
    """Fetch a LinkedIn company's recent posts: text, reactions, comments."""
    if err := _check_key():
        return err
    try:
        resp = requests.post(f"{API_BASE}/api/v1/linkedin/company/posts", headers=HEADERS(), json={"company": company}, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


@tool
def scavio_linkedin_search_jobs(search: str, location: str = "") -> str:
    """Search LinkedIn job listings by keyword and optional location."""
    if err := _check_key():
        return err
    body: dict = {"search": search}
    if location:
        body["location"] = location
    try:
        resp = requests.post(f"{API_BASE}/api/v1/linkedin/search/jobs", headers=HEADERS(), json=body, timeout=60)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    if resp.status_code >= 400:
        return f"API error {resp.status_code}: {resp.text[:500]}"
    return json.dumps(resp.json().get("data", {}), indent=2, ensure_ascii=False)[:8000]


SYSTEM_PROMPT = """\
You are LinkedInLeadFinder. Given a target company and optional role \
keywords, produce a B2B intelligence brief for sales outreach.

## Parse the brief

Extract: target company name (the LinkedIn company slug if obvious),
role keywords or department focus, and any context about the user's
product or pitch.

## Workflow

1. COMPANY PROFILE
   Call scavio_linkedin_company with the company slug. Extract:
   description, industry, employee count, HQ location, specialties,
   and the featured_employees sample.

2. RECENT ACTIVITY
   Call scavio_linkedin_company_posts. Identify what the company
   is talking about: product launches, hiring pushes, thought
   leadership themes. These are engagement hooks.

3. HIRING SIGNALS
   Call scavio_linkedin_search_jobs with the company name plus the
   role keywords. Active hiring in a department signals budget and
   growth -- prime outreach timing.

4. SYNTHESIZE
   Return:

   COMPANY: <name>
   Industry: <industry> | Size: <employee range> | HQ: <location>
   Tagline: <one-line description>

   GROWTH SIGNALS
   - <what they are hiring for, how many open roles found>
   - <recent post themes suggesting strategic priorities>

   FEATURED CONTACTS
   - <name> -- <title> (from featured_employees)
   - ...
   (These are public LinkedIn profiles the company chose to spotlight.)

   ENGAGEMENT ANGLES
   - <specific post or initiative to reference in outreach>
   - <hiring area that aligns with user's product>

   OUTREACH SUGGESTION
   <2-3 sentences: who to reach, what hook to lead with, what value
   to offer>

## Rules
- Only report data from tool results. Never invent names or titles.
- Keep under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [scavio_linkedin_company, scavio_linkedin_company_posts, scavio_linkedin_search_jobs]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = (
    "Microsoft, looking for AI and cloud engineering leaders to pitch "
    "our developer productivity tool"
)


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
