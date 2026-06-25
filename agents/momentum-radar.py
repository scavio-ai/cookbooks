"""
MomentumRadar: score a topic's momentum across four platforms at once.

A free alternative to multi-tool trend dashboards. Give it a topic or product.
It checks Google (search interest + news), YouTube (are creators covering it),
TikTok (is it spreading), and Reddit (are people discussing it), then synthesizes
a single momentum read: rising, steady, or fading -- with the evidence per
platform. Built for product hunters, marketers, and dropshippers.

Built with LangChain create_agent, OpenAI tool calling, and langchain-scavio.

Prerequisites:
  pip install langchain langchain-openai "langchain-scavio>=2.9" python-dotenv
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev
  export OPENAI_API_KEY="sk-..."

Usage:
  python agents/momentum-radar.py "stanley quencher dupes"
"""

import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_scavio import (
    ScavioRedditSearch,
    ScavioSearch,
    ScavioTikTokSearchVideos,
    ScavioYouTubeSearch,
)

load_dotenv(override=True)


SYSTEM_PROMPT = """You are MomentumRadar. Given a topic or product, judge its
cross-platform momentum.

## Workflow

1. GATHER (one call per platform; add a second only if needed):
   - ScavioSearch: gauge demand and recency from organic results, news, and
     related searches.
   - ScavioYouTubeSearch (sort by recent/views): are creators making videos?
   - ScavioTikTokSearchVideos (recent): is it spreading on TikTok? Look at
     view/like counts on returned videos.
   - ScavioRedditSearch (sort=new): are people actively discussing it?

2. SCORE each platform 0-3 for momentum (0 dead, 3 hot), citing one concrete
   signal each (a recent date, a high view count, an active thread).

3. ANSWER:

   # Momentum: <topic>
   Overall: <Rising | Steady | Fading>  (total /12)

   - Google  <score>/3  -- <signal>
   - YouTube <score>/3  -- <signal>
   - TikTok  <score>/3  -- <signal>
   - Reddit  <score>/3  -- <signal>

   Verdict: <2-3 sentences on whether to act now and why>

## Rules
- Base every signal on returned data. Never invent counts, dates, or threads.
- Keep the answer under 400 words.
"""


def build_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [
        ScavioSearch(max_results=6),
        ScavioYouTubeSearch(max_results=6),
        ScavioTikTokSearchVideos(max_results=8),
        ScavioRedditSearch(max_results=8),
    ]
    return create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)


def run(topic: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": topic}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) or "stanley quencher dupes"
    print(f"\nTopic: {topic}\n{'-' * 60}")
    print(run(topic))
