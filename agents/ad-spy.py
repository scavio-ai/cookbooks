"""
AdSpy: AI competitive ad intelligence agent.

A free alternative to AdBeat, Pathmatics, and PowerAdSpy for competitive
ad research. Give it a brand name. It searches the Meta Ad Library, Google
Ads Transparency Center, and LinkedIn Ad Library for active campaigns and
returns a competitive ad brief.

Built with LangChain create_agent, OpenAI tool calling, and the Scavio
real-time search API (Meta Ads, Google Ads, LinkedIn Ads endpoints).

Prerequisites:
  pip install langchain langchain-openai python-dotenv requests

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/ad-spy.py "Notion"
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
def scavio_meta_ads_search(query: str) -> str:
    """Search the Meta Ad Library (Facebook/Instagram) for ads matching a keyword."""
    return _post("/api/v1/meta-ads/search", {"query": query})


@tool
def scavio_googleads_advertisers(query: str) -> str:
    """Look up advertisers in Google Ads Transparency Center by name or domain."""
    return _post("/api/v1/googleads/advertisers", {"query": query})


@tool
def scavio_googleads_search(advertiser_id: str) -> str:
    """Get ads for a Google advertiser by their advertiser id (starts with AR)."""
    return _post("/api/v1/googleads/search", {"advertiser_id": advertiser_id})


@tool
def scavio_linkedin_ads_search(keyword: str) -> str:
    """Search ads in the LinkedIn Ad Library by keyword."""
    return _post("/api/v1/linkedin/ads/search", {"keyword": keyword})


SYSTEM_PROMPT = """\
You are AdSpy. Given a brand name, produce a competitive ad intelligence
brief by searching across Meta, Google, and LinkedIn ad libraries.

## Workflow

1. META ADS
   Call scavio_meta_ads_search with the brand name. Note ad count, ad
   formats (image, video, carousel), and messaging themes.

2. GOOGLE ADS
   Call scavio_googleads_advertisers with the brand name to find the
   advertiser id. Then call scavio_googleads_search with that id. Note
   ad formats, landing pages, and creative themes.

3. LINKEDIN ADS
   Call scavio_linkedin_ads_search with the brand name. Note ad formats,
   targeting signals (B2B vs B2C), and messaging.

4. SYNTHESIZE AND ANSWER
   Return a brief with these sections:

   PLATFORM PRESENCE
   - Which platforms have active ads, roughly how many on each

   AD FORMATS
   - Breakdown of formats used (image, video, carousel, text)

   MESSAGING THEMES
   - 3-5 recurring copy themes across platforms (e.g. "free trial",
     "enterprise security", "customer testimonials")

   CREATIVE PATTERNS
   - Common visual or CTA patterns observed

   COMPETITIVE SIGNAL
   - One paragraph: where is this brand spending heaviest, and what
     does the messaging emphasis suggest about their current GTM?

## Rules
- Only cite ad copy and formats that appeared in API responses.
- If a platform returns no ads, report that -- do not fabricate.
- Keep the final answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [
        scavio_meta_ads_search,
        scavio_googleads_advertisers,
        scavio_googleads_search,
        scavio_linkedin_ads_search,
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brand: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brand}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = "Notion"


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrand: {brief}\n{'-' * 60}")
    print(run(brief))
