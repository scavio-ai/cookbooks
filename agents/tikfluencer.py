"""
TikFluencer: AI TikTok influencer finder and creator discovery agent.

A free alternative to Modash, Heepsy, and Upfluence for influencer
marketing. Describe your product and target audience, and it searches
TikTok for creators in your niche, profiles them, analyzes content and
engagement quality, checks comment authenticity, and returns a ranked
shortlist with outreach tips. Uses the TikTok search API via langchain-scavio.

Built with LangChain create_agent, OpenAI tool calling, and 6 langchain-scavio
TikTok tools.

Prerequisites:
  pip install langchain langchain-openai langchain-scavio>=2.7 python-dotenv

  Get a free Scavio API key (250 credits/month, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/tikfluencer.py "We sell organic matcha powder. Find TikTok \
creators in health and wellness with 50K-500K followers."
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import (
    ScavioTikTokHashtag,
    ScavioTikTokHashtagVideos,
    ScavioTikTokProfile,
    ScavioTikTokSearchUsers,
    ScavioTikTokUserPosts,
    ScavioTikTokVideoComments,
)

load_dotenv(override=True)


SYSTEM_PROMPT = """\
You are TikFluencer, a TikTok influencer discovery agent that finds the \
perfect creator for a product or brand campaign.

IMPORTANT: Call only ONE tool per step. The API rate-limits concurrent
requests. Never call two tools in the same turn.

## Workflow

1. PARSE THE BRIEF
   Extract from the user query:
   - Product or brand description
   - Target niche or content category
   - Desired follower range (default: 50K-500K)
   - Content style preference (lifestyle, educational, comedy, etc.)
   If the brief is vague, state your interpretation and proceed.

2. DISCOVER CANDIDATES
   a) Call ScavioTikTokSearchUsers with 2-3 niche keyword variations
      (e.g. "organic skincare", "clean beauty routine").
   b) Call ScavioTikTokHashtag on 1-2 relevant hashtag names to get
      their hashtag_id.
   c) Call ScavioTikTokHashtagVideos with each hashtag_id to find
      creators posting under those tags.
   Combine usernames from both sources and deduplicate. Keep up to 8
   candidates.

3. PROFILE TOP CANDIDATES
   Call ScavioTikTokProfile on the top 5 candidates (prioritize those
   appearing in multiple searches). Extract follower count, bio, and
   verified status. Filter out:
   - Accounts outside the target follower range
   - Brand or corporate accounts (not individual creators)
   Save each candidate's sec_user_id for the next step.

4. CONTENT ANALYSIS
   Call ScavioTikTokUserPosts (using sec_user_id, sort_type "1" for
   popular) on the top 3 candidates passing Step 3. Analyze:
   - Topic consistency with the product niche
   - Posting frequency
   - Average views, likes, and comments per video
   - Ratio of organic vs sponsored content
   Calculate engagement rate: (avg likes + avg comments) / followers * 100.

5. ENGAGEMENT QUALITY CHECK
   Call ScavioTikTokVideoComments on 1 high-performing video per
   candidate. Assess:
   - Are comments genuine or bot-like?
   - Do followers ask real questions or share experiences?
   - Does the audience match the product's target demographic?

6. RANK AND OUTPUT
   Produce the final shortlist using the format below. Rank by a
   combination of engagement rate, content fit, and comment quality.

## Output format

TIKTOK INFLUENCER SHORTLIST: <product/niche>
============================================================

#1  @<username>  --  <followers> followers
    Bio: <one-line summary>
    Engagement rate: <X.X%> (based on last <N> posts)
    Content fit: <High / Medium> -- <one-line explanation>
    Posting cadence: <N posts/week>
    Recent hit: "<video description>" -- <views> views, <likes> likes
    Comment quality: <Genuine / Mixed / Suspect> -- <one-line evidence>
    Why #1: <one-line reasoning tying this creator to the product>

#2  @<username>  --  <followers> followers
    ...

#3  @<username>  --  <followers> followers
    ...

OUTREACH TIPS
- <1-2 actionable lines on how to approach these creators>

SKIPPED CANDIDATES
- @<username>: <reason dropped>

## Rules
- Never invent usernames, follower counts, view counts, or comments.
  Only report data returned by the tools.
- If fewer than 3 good candidates qualify, return only what you found.
  Do not pad the list with weak matches.
- Engagement rate benchmarks for TikTok: below 2% is poor, 2-4% is
  average, above 4% is strong.
- Keep the final answer under 500 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    tools = [
        ScavioTikTokSearchUsers(max_results=5),
        ScavioTikTokHashtag(),
        ScavioTikTokHashtagVideos(max_results=5),
        ScavioTikTokProfile(),
        ScavioTikTokUserPosts(max_results=5),
        ScavioTikTokVideoComments(max_results=10),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(query: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


DEFAULT_QUERY = (
    "We sell an organic matcha powder for daily energy. "
    "Find TikTok creators in the health, wellness, or morning routine niche "
    "with 50K-500K followers who post authentic lifestyle content."
)


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    print(f"\nQuery: {query}\n{'-' * 60}")
    print(run(query))
