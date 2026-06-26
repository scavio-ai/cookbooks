"""
InstagramScout: AI Instagram creator-discovery agent for brand campaigns.

A free alternative to Modash, Heepsy, and Upfluence for finding Instagram
creators. Give it a campaign brief (niche + vibe). It searches Instagram users
and hashtags, profiles the strongest candidates, and returns a ranked
shortlist with follower counts and a one-line fit rationale each.

Built with LangChain create_agent, OpenAI tool calling, and langchain-scavio
Instagram tools.

Prerequisites:
  pip install langchain langchain-openai "langchain-scavio>=2.9" python-dotenv

  Free Scavio API key (50 free credits, no card): https://dashboard.scavio.dev
  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/instagram-scout.py "sustainable home goods creators for a DTC \
brand launch, aesthetic and craft-focused, 10k-200k followers"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import (
    ScavioInstagramSearchHashtags,
    ScavioInstagramSearchUsers,
)

load_dotenv(override=True)


SYSTEM_PROMPT = """You are InstagramScout. Given a brand's campaign brief, \
build a vetted shortlist of Instagram creators to approach.

## Workflow

1. PARSE THE BRIEF
   Extract the niche, the desired aesthetic/vibe, and any follower range or
   constraints. State your interpretation in one line.

2. SEARCH
   - Call ScavioInstagramSearchUsers with 2-3 keyword variants for the niche.
     Each result carries the handle, full name, follower_count, and a verified
     flag -- enough to judge fit and size.
   - Call ScavioInstagramSearchHashtags on 1-2 niche hashtags to gauge topic
     volume (media_count) and surface adjacent terms.
   Deduplicate handles across searches.

3. JUDGE FIT
   Using the search-result fields, keep creators whose follower_count falls in
   the requested range and whose name/handle signals the niche. Note the
   hashtag volumes as evidence the niche is active.

4. RANK AND ANSWER
   Return the top 5 creators, best fit first:

   #N  @handle  --  <follower_count> followers
   Focus: <what they post, inferred from handle/name>
   Fit: <one line tying them to the brief>

   End with one line of outreach advice specific to this niche.

## Rules
- Only list handles that actually appeared in search results. Never invent
  handles, follower counts, or bios.
- If fewer than 5 strong fits exist, return only the real ones.
- Keep the final answer under 350 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [
        ScavioInstagramSearchUsers(max_results=12),
        ScavioInstagramSearchHashtags(max_results=8),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = (
    "specialty coffee creators for a roaster's subscription launch; warm, "
    "craft-focused aesthetic; 10k-250k followers"
)


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
