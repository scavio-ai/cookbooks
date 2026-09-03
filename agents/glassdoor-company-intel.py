"""
GlassdoorCompanyIntel: AI employer brand intelligence agent.

A free alternative to Comparably and RepVue for employer brand research.
Give it a company name. It looks up the company on Glassdoor, reads
reviews and salary data, and returns an employer brand brief.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
real-time search API (Glassdoor endpoints).

Prerequisites:
  pip install langchain langchain-openai python-dotenv requests

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/glassdoor-company-intel.py "Stripe"
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
def scavio_glassdoor_companies(query: str) -> str:
    """Look up a company name on Glassdoor and return matching employer ids."""
    return _post("/api/v1/glassdoor/companies", {"query": query})


@tool
def scavio_glassdoor_company(employer_id: str) -> str:
    """Get the full Glassdoor company profile by employer id."""
    return _post("/api/v1/glassdoor/company", {"employer_id": employer_id})


@tool
def scavio_glassdoor_reviews(employer_id: str) -> str:
    """Get Glassdoor reviews for a company by employer id."""
    return _post("/api/v1/glassdoor/reviews", {"employer_id": employer_id})


@tool
def scavio_glassdoor_salaries(employer_id: str) -> str:
    """Get Glassdoor salary data for a company by employer id."""
    return _post("/api/v1/glassdoor/salaries", {"employer_id": employer_id})


SYSTEM_PROMPT = """\
You are GlassdoorCompanyIntel. Given a company name, produce an employer
brand intelligence brief.

## Workflow

1. RESOLVE COMPANY
   Call scavio_glassdoor_companies with the company name. Pick the best
   match and note its employer_id.

2. COMPANY PROFILE
   Call scavio_glassdoor_company with the employer_id. Note the overall
   rating, CEO approval, recommend-to-friend %, and category ratings.

3. REVIEWS
   Call scavio_glassdoor_reviews with the employer_id. Read the most
   recent reviews. Identify recurring praise and complaint themes.

4. SALARIES
   Call scavio_glassdoor_salaries with the employer_id. Note salary
   ranges for the most-reported roles.

5. SYNTHESIZE AND ANSWER
   Return a brief with these sections:

   EMPLOYER SCORECARD
   - Overall rating (out of 5), CEO approval %, recommend %
   - Category ratings: culture, work-life balance, comp, management

   TOP PRAISE (3 themes)
   - What employees consistently praise, with quoted evidence

   TOP COMPLAINTS (3 themes)
   - What employees consistently criticize, with quoted evidence

   SALARY SNAPSHOT
   - 3-5 most-reported roles with their salary range

   CULTURE SIGNAL
   - One paragraph: what kind of person thrives here vs. who should
     steer clear? Support with review evidence.

## Rules
- Only cite ratings and quotes that appeared in API responses.
- If salary data is sparse, say so.
- Keep the final answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [
        scavio_glassdoor_companies,
        scavio_glassdoor_company,
        scavio_glassdoor_reviews,
        scavio_glassdoor_salaries,
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(company: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": company}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "Stripe"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nCompany: {brief}\n{'-' * 60}")
    print(run(brief))
