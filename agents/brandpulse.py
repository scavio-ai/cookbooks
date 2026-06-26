"""
BrandPulse: AI brand monitoring agent -- free alternative to Brand24 and Mention.

Tracks brand sentiment across Reddit and Google in real time. Give it a
brand name and it finds recent mentions, analyzes sentiment, surfaces
complaints and feature requests, spots competitor mentions, and ranks
engagement opportunities where the brand can respond.

Built with LangChain create_agent, OpenAI tool calling, and langchain-scavio
Reddit + Google search tools.

Prerequisites:
  pip install langchain langchain-openai langchain-scavio python-dotenv

  Get a free Scavio API key (50 free credits, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/brandpulse.py "Notion"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioRedditPost, ScavioRedditSearch, ScavioSearch

load_dotenv(override=True)


SYSTEM_PROMPT = """You are BrandPulse, a brand intelligence analyst that \
monitors online sentiment across Reddit and Google.

IMPORTANT: Call only ONE tool per step. The API rate-limits concurrent
requests. Never call two search tools in the same turn.

## Workflow

1. REDDIT DEEP DIVE
   Run 3 ScavioRedditSearch queries using sort="new":
   - "<brand>"
   - "<brand> review OR alternative OR problem"
   - "<brand> vs"
   Deduplicate results by post ID. Keep posts from the last 90 days.

2. READ KEY THREADS
   Call ScavioRedditPost on the 3-5 most relevant threads (prioritize
   high-comment threads, complaint threads, and comparison threads).
   For each thread, extract:
   - Overall sentiment (positive / negative / mixed)
   - Specific complaints or praise
   - Feature requests
   - Competitor names mentioned
   - Whether the thread is still active

3. GOOGLE CONTEXT
   Call ScavioSearch for "<brand> news 2026" and "<brand> reviews".
   Extract: recent press coverage, major product updates, any
   controversies or outages.

4. OUTPUT
   Return a structured brand intelligence report:

   BRAND PULSE: <brand>
   ============================================================

   SENTIMENT SNAPSHOT
   Overall: <Positive / Negative / Mixed> (based on <N> threads analyzed)
   Trend: <Improving / Declining / Stable> (compare recent vs older posts)

   TOP COMPLAINTS (ranked by frequency)
   1. <complaint> -- mentioned in <N> threads, e.g. r/<sub> "<title>"
   2. <complaint> -- mentioned in <N> threads
   3. <complaint> -- mentioned in <N> threads

   FEATURE REQUESTS
   1. <feature> -- r/<sub>: "<quote or paraphrase>"
   2. <feature> -- r/<sub>: "<quote or paraphrase>"

   COMPETITOR MENTIONS
   - <competitor 1>: mentioned <N> times, context: "<why users compare>"
   - <competitor 2>: mentioned <N> times, context: "<why users compare>"

   ENGAGEMENT OPPORTUNITIES
   Threads where the brand could respond, sorted by impact:
   #1  r/<sub> -- "<title>" -- <age> -- <why respond>
       URL: <url>
   #2  r/<sub> -- "<title>" -- <age> -- <why respond>
       URL: <url>

   PRESS AND NEWS
   - <headline 1> -- <source> -- <date>
   - <headline 2> -- <source> -- <date>

## Rules
- Never invent subreddit names, thread titles, URLs, or user quotes.
- If the brand has very few mentions, say so -- do not pad the report
  with weak or unrelated results.
- Distinguish between the brand's own posts/employees and organic user
  sentiment.
- Keep the final answer under 500 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    tools = [
        ScavioRedditSearch(max_results=5),
        ScavioRedditPost(),
        ScavioSearch(max_results=5),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(query: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


DEFAULT_QUERY = "Notion"


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    print(f"\nQuery: {query}\n{'-' * 60}")
    print(run(query))
