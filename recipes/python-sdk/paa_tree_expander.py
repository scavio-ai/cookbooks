"""
paa_tree_expander.py -- breadth-first keyword + People-Also-Ask expander.

Starts from a seed keyword, walks Google "related searches" breadth-first to
a fixed depth, and collects every People-Also-Ask question along the way.
Writes a flat CSV (depth, parent, term, type) you can cluster for SEO content
planning. A free alternative to AnswerThePublic and Keyword Sheeter.

Uses the Scavio Python SDK -- no LLM required.

Prerequisites:
  pip install scavio python-dotenv
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev

Usage:
  python paa_tree_expander.py "project management software" --depth 2 --out paa.csv
"""

import argparse
import csv
import sys
from collections import deque

from dotenv import load_dotenv
from scavio import ScavioClient

load_dotenv(override=True)


def question_text(q):
    """PAA items come back as strings or dicts depending on the SERP."""
    if isinstance(q, dict):
        return q.get("question") or q.get("title") or q.get("query")
    return q


def expand(seed: str, depth: int):
    client = ScavioClient()
    rows = []
    seen = {seed}
    queue = deque([(seed, 0, "")])

    while queue:
        term, level, parent = queue.popleft()
        resp = client.google.search(term)

        for q in resp.get("questions") or []:
            text = question_text(q)
            if text:
                rows.append({"depth": level, "parent": term, "term": text, "type": "paa"})

        for rel in resp.get("related_searches") or []:
            kw = rel.get("query") if isinstance(rel, dict) else rel
            if not kw or kw in seen:
                continue
            seen.add(kw)
            rows.append({"depth": level, "parent": term, "term": kw, "type": "related"})
            if level < depth:
                queue.append((kw, level + 1, term))

    return rows


def main():
    ap = argparse.ArgumentParser(description="Expand a seed keyword into a PAA/related CSV.")
    ap.add_argument("seed", nargs="*", default=["project management software"])
    ap.add_argument("--depth", type=int, default=1, help="related-search crawl depth (default 1)")
    ap.add_argument("--out", default="paa_tree.csv")
    args = ap.parse_args()

    seed = " ".join(args.seed) if args.seed else "project management software"
    print(f"Expanding '{seed}' to depth {args.depth} ...", file=sys.stderr)
    rows = expand(seed, args.depth)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["depth", "parent", "term", "type"])
        writer.writeheader()
        writer.writerows(rows)

    paa = sum(1 for r in rows if r["type"] == "paa")
    rel = sum(1 for r in rows if r["type"] == "related")
    print(f"Wrote {len(rows)} rows ({paa} PAA questions, {rel} related searches) to {args.out}")


if __name__ == "__main__":
    main()
