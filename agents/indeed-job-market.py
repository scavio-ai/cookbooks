"""
IndeedJobMarket: AI job market intelligence agent.

A free alternative to LinkedIn Talent Insights and Lightcast for sizing up
a job market. Give it a role and location. It searches Indeed listings,
reads job details, and checks employer profiles -- then returns a market
intelligence brief.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
real-time search API (Indeed endpoints).

Prerequisites:
  pip install langchain langchain-openai python-dotenv requests

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/indeed-job-market.py "data engineer in San Francisco"
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
def scavio_indeed_search(query: str, location: str = "") -> str:
    """Search Indeed jobs by keyword and optional location."""
    body: dict = {"query": query}
    if location:
        body["location"] = location
    return _post("/api/v1/indeed/search", body)


@tool
def scavio_indeed_job(job_id: str) -> str:
    """Get full details for an Indeed job listing by its job key or URL."""
    return _post("/api/v1/indeed/job", {"job_id": job_id})


@tool
def scavio_indeed_company(company: str) -> str:
    """Get an Indeed company profile: ratings, reviews summary, size."""
    return _post("/api/v1/indeed/company", {"company": company})


SYSTEM_PROMPT = """\
You are IndeedJobMarket. Given a role and location, produce a job market
intelligence brief.

## Workflow

1. SEARCH JOBS
   Call scavio_indeed_search with the role (and location if given). Note
   job titles, companies, salary ranges, and posting dates.

2. DEEP-READ LISTINGS
   Pick 3-4 representative listings (mix of seniority, company size).
   Call scavio_indeed_job on each. Note: required skills, salary details,
   remote/hybrid/onsite, benefits, experience level.

3. EMPLOYER PROFILES
   Call scavio_indeed_company on 2-3 of the top hiring companies. Note
   their Indeed rating and size.

4. SYNTHESIZE AND ANSWER
   Return a brief with these sections:

   MARKET OVERVIEW
   - Number of active listings found
   - Salary range (low / median / high) from the listings examined

   TOP EMPLOYERS
   - 3-5 companies hiring, with their Indeed rating and rough headcount

   SKILL DEMAND
   - The 5-8 most-requested skills/technologies across listings

   WORK MODE SPLIT
   - Estimate of remote vs hybrid vs onsite from listings examined

   MARKET SIGNAL
   - One paragraph: is this role in high demand, balanced, or cooling?
     Support with posting volume and salary evidence.

## Rules
- Only cite numbers that appeared in API responses.
- If salary is not disclosed on a listing, skip it in the range calc.
- Keep the final answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [scavio_indeed_search, scavio_indeed_job, scavio_indeed_company]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "data engineer in San Francisco"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
