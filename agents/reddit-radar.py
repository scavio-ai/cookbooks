"""
RedditRadar: find live Reddit threads where you can authentically engage to
surface your product.

Reddit is one of the highest-converting channels for indie hackers and SaaS
founders -- but the work is hunting for the *right* conversations: someone
asking for exactly what you built, in a subreddit that tolerates soft-promo,
in a thread that is still active. RedditRadar automates that hunt.

Give it your product and keywords. It expands into Reddit-intent queries,
searches new posts, filters for unresolved asks, reads the ones that qualify,
and ranks the best engagement opportunities.

Prerequisites:
  pip install langchain langchain-openai langchain-scavio python-dotenv

  Get a free Scavio API key (500 credits/month, no credit card):
    https://dashboard.scavio.dev

  export SCAVIO_API_KEY="sk_..."
  export OPENAI_API_KEY="sk-..."

Usage:
  python reddit-radar.py "Scavio is a real-time search API for AI agents -- \
a free alternative to SerpAPI. Find threads where people ask for serpapi \
alternatives, amazon product APIs, or langchain search tools."
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import ScavioRedditPost, ScavioRedditSearch

load_dotenv(override=True)


SYSTEM_PROMPT = """You are RedditRadar. Given a founder's product brief, \
find live Reddit threads where they can authentically engage to surface \
their product.

## Parse the brief

The user will provide a natural-language brief that contains:
- A 1-2 sentence product description
- Keywords or phrases describing the problem it solves or alternatives it
  competes with

Extract both. If the brief is vague, state your best interpretation briefly
and proceed.

## Workflow

1. EXPAND INTENT QUERIES
   From the keywords, generate 3-4 Reddit-intent search variants. Mix shapes:
   - "<keyword> alternative"
   - "anyone know a tool for <problem>"
   - "looking for <capability>"
   - "<competitor> sucks" / "replace <competitor>"
   - "best <category> 2026"
   Prepend "subreddit:Name" only when a single sub is an obvious fit;
   otherwise search across Reddit.

2. SEARCH
   Call ScavioRedditSearch for each intent variant with sort="new".
   Combine results across searches and deduplicate by post id.

3. SHORT-LIST (no extra API calls)
   Using only the search-response fields (title, subreddit, author,
   timestamp), keep threads that:
   - Are less than 30 days old; prefer less than 7
   - Sit in subreddits where soft-promo is tolerated (builder, marketer,
     problem-space, or product-discovery subs); skip news, meme, and
     explicitly no-promo subs
   - Have titles consistent with an unresolved need: question words,
     "looking for", "alternative to", "recommend", "stuck", "help",
     "tool for", "how do I"
   Cap the short-list at 5 candidates.

4. DEEP READ
   Call ScavioRedditPost on each short-listed URL. Read the OP body to
   confirm the ask is real (not a promo post, not a troll). Scan the top
   non-AutoModerator comments -- if a dominant answer has clearly won the
   thread, drop it from the output.

5. RANK AND ANSWER
   Return the top 3-5 threads ranked by engagement potential. Format:

   #N  r/<subreddit>  --  <relative age, e.g. "2 days ago">
   Thread: <title>
   URL: <full url>
   Score: <N>/10  (recency + fit + openness)
   OP is asking: <one-line paraphrase of the real need>
   Why it fits: <one line tying product capability to OP's ask>
   Angle: <specific value-first opener -- NOT a pre-written comment>

   Finish with one line: "Lead with value. Disclose you are the founder.
   Do not paste the same comment across threads."

## Rules
- Never invent titles, URLs, subreddits, authors, timestamps, or scores.
- If fewer than 3 good threads qualify, return only what you found --
  do not pad with weak matches.
- Keep the final answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [
        ScavioRedditSearch(max_results=10),
        ScavioRedditPost(),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(brief: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": brief}]})
    return result["messages"][-1].content


DEFAULT_BRIEF = (
    "Scavio is a real-time search API for AI agents -- a free alternative "
    "to SerpAPI with 500 credits/month. Find threads where people ask for "
    "SerpAPI alternatives, Amazon product APIs, or LangChain search tools."
)


if __name__ == "__main__":
    brief = " ".join(sys.argv[1:]) or DEFAULT_BRIEF
    print(f"\nBrief: {brief}\n{'-' * 60}")
    print(run(brief))
