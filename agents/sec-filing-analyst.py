"""
SECFilingAnalyst: AI public-company filing analysis agent.

A free alternative to AlphaSense, Sentieo, and Koyfin for SEC filing
research. Give it a company name or ticker. It looks up the company
via SEC EDGAR, reads recent filings, checks XBRL financial facts, and
returns an analyst brief: filing cadence, revenue/income trends, risk
factor highlights, and notable disclosures.

Built with LangChain create_agent, OpenAI tool calling, and custom
Scavio API tools for SEC EDGAR data.

Prerequisites:
  pip install langchain langchain-openai requests python-dotenv

  Get a free Scavio API key (50 free credits, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/sec-filing-analyst.py "AAPL"
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
def scavio_sec_lookup(query: str) -> str:
    """Look up a company on SEC EDGAR by ticker or name. Returns CIK, name, ticker, exchange, and match tier."""
    return _post("/api/v1/sec/lookup", {"query": query})


@tool
def scavio_sec_company(ticker: str) -> str:
    """Get SEC EDGAR company details by ticker or CIK: name, SIC, state, addresses, former names, and filing counts."""
    return _post("/api/v1/sec/company", {"ticker": ticker})


@tool
def scavio_sec_filings(ticker: str) -> str:
    """Get recent SEC filings by ticker or CIK: form type, date, description, and accession number for each filing."""
    return _post("/api/v1/sec/filings", {"ticker": ticker})


@tool
def scavio_sec_facts(ticker: str) -> str:
    """Get XBRL financial facts for a company: revenue, net income, assets, and other reported values with their periods."""
    return _post("/api/v1/sec/facts", {"ticker": ticker})


SYSTEM_PROMPT = """You are SECFilingAnalyst. Given a company name or ticker, \
produce an analyst brief from real SEC EDGAR data.

## Workflow

1. RESOLVE
   Call scavio_sec_lookup with the query. Confirm the correct entity
   (ticker, CIK, exchange). If ambiguous, pick the most liquid US listing.

2. COMPANY PROFILE
   Call scavio_sec_company with the ticker to get SIC code, state of
   incorporation, and filing history summary.

3. RECENT FILINGS
   Call scavio_sec_filings with the ticker. Note the last 10 filings:
   form types (10-K, 10-Q, 8-K, etc.), dates, and descriptions. Flag
   any unusual or non-routine filings (S-1, SC 13D, DEFA14A, etc.).

4. FINANCIAL FACTS
   Call scavio_sec_facts with the ticker. Extract revenue and net income
   across available periods to identify trends. Note the most recent
   annual and quarterly values.

5. REPORT
   Return a structured analyst brief:

   COMPANY: <name> (<ticker>) -- <exchange>
   CIK: <cik> | SIC: <sic_code> <sic_description>
   Incorporated: <state>

   RECENT FILINGS (last 90 days)
   - <date> <form_type>: <description>
   - ...

   FINANCIAL TREND
   Revenue: <most recent annual> -> <trend direction>
   Net Income: <most recent annual> -> <trend direction>
   <any notable year-over-year changes>

   NOTABLE SIGNALS
   - <any unusual filing types or patterns>
   - <any insider transaction forms (Form 4) frequency>
   - <any material events (8-K themes)>

   ANALYST TAKE
   <one paragraph: what stands out and what to watch>

## Rules
- Only report data from actual SEC EDGAR results. Never fabricate
  filing dates, financial figures, or form types.
- If financial facts are sparse (private or foreign filer), say so
  explicitly rather than guessing.
- Keep the final answer under 500 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [scavio_sec_lookup, scavio_sec_company, scavio_sec_filings, scavio_sec_facts]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "AAPL"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
