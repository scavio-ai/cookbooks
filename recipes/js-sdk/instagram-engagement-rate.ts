/**
 * instagram-engagement-rate.ts -- compute a creator's real engagement rate.
 *
 * Pulls a public Instagram profile plus its recent posts and computes the
 * engagement rate (avg likes + comments per post / followers) -- the single
 * number influencer marketers actually care about. Free alternative to the
 * "engagement rate" paywalls in HypeAuditor / Modash.
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."
 *
 * Cost: profile is 8 credits, user posts is 2, so a full run costs 10.
 *
 * Run:
 *   npm run instagram-engagement -- nike
 */
import { Scavio } from "scavio";

const username = process.argv[2] || "nike";
const client = new Scavio({ apiKey: process.env.SCAVIO_API_KEY });

const profile: any = (await client.instagram.profile({ username })).data ?? {};
const followers: number = profile.follower_count ?? 0;

const feed: any = (await client.instagram.userPosts({ username, count: 12 })).data ?? {};
const posts: any[] = feed.items ?? [];

const totals = posts.reduce(
  (acc, p) => {
    acc.likes += p.like_count ?? 0;
    acc.comments += p.comment_count ?? 0;
    return acc;
  },
  { likes: 0, comments: 0 },
);

const n = posts.length || 1;
const avgLikes = totals.likes / n;
const avgComments = totals.comments / n;
const engagementRate = followers ? ((avgLikes + avgComments) / followers) * 100 : 0;

console.log(
  JSON.stringify(
    {
      username,
      verified: profile.is_verified ?? false,
      followers,
      posts_sampled: posts.length,
      avg_likes: Math.round(avgLikes),
      avg_comments: Math.round(avgComments),
      engagement_rate_pct: Number(engagementRate.toFixed(2)),
    },
    null,
    2,
  ),
);
