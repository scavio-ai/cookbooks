"""
instagram_follower_overlap.py -- accounts two Instagram profiles both follow.

Pulls the "following" lists of two public Instagram accounts (paginating up to
a cap) and prints the overlap -- the accounts they both follow. A fast way to
map a niche: who do two competing brands or two creators in a space both pay
attention to.

The followings endpoint costs 8 credits per page (default cap = 2 pages each,
so 32 credits for the two accounts at the default).

Prerequisites:
  pip install scavio python-dotenv
  export SCAVIO_API_KEY="sk_..."

Usage:
  python instagram_follower_overlap.py natgeo nasa --pages 2
"""

import argparse
import sys

from dotenv import load_dotenv
from scavio import ScavioClient

load_dotenv(override=True)


def following_set(client: ScavioClient, username: str, pages: int) -> dict:
    """Return {username_lower: display_name} for who `username` follows."""
    out, cursor = {}, None
    for _ in range(pages):
        kwargs = {"username": username, "count": 100}
        if cursor:
            kwargs["cursor"] = cursor
        data = client.instagram.user_followings(**kwargs).get("data") or {}
        for u in data.get("users") or []:
            handle = (u.get("username") or "").lower()
            if handle:
                out[handle] = u.get("full_name") or ""
        cursor = data.get("next_max_id")
        if not data.get("has_more") or not cursor:
            break
    return out


def main():
    ap = argparse.ArgumentParser(description="Find the Instagram-following overlap of two accounts.")
    ap.add_argument("account_a", nargs="?", default="natgeo")
    ap.add_argument("account_b", nargs="?", default="nasa")
    ap.add_argument("--pages", type=int, default=2, help="max pages per account (100/page)")
    args = ap.parse_args()

    client = ScavioClient()
    print(f"Fetching followings for @{args.account_a} and @{args.account_b} ...", file=sys.stderr)
    a = following_set(client, args.account_a, args.pages)
    b = following_set(client, args.account_b, args.pages)

    overlap = sorted(set(a) & set(b))
    print(f"\n@{args.account_a}: {len(a)} sampled   @{args.account_b}: {len(b)} sampled")
    print(f"Both follow {len(overlap)} of the sampled accounts:\n")
    for handle in overlap:
        print(f"  @{handle:<24} {a[handle]}")
    if not overlap:
        print("  (no overlap in the sampled pages -- raise --pages to widen the sample)")


if __name__ == "__main__":
    main()
