/**
 * tiktok-creator-scorecard.ts -- a one-call scorecard for TikTok creators.
 *
 * Searches TikTok creators by keyword and prints a ranked scorecard:
 * followers, total likes, video count, and a likes-per-follower "affinity"
 * signal. The starting point for influencer shortlisting -- a free
 * alternative to Modash / Heepsy creator search.
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."
 *
 * Run:
 *   npm run tiktok-scorecard -- "specialty coffee"
 */
import { Scavio } from "scavio";

const keyword = process.argv.slice(2).join(" ") || "specialty coffee";
const client = new Scavio({ apiKey: process.env.SCAVIO_API_KEY });

const res: any = await client.tiktok.searchUsers({ keyword, count: 15 });
const users: any[] = res.data?.user_list ?? [];

const rows = users
  .map((u) => u.user_info ?? {})
  .filter((info) => info.uid)
  .map((info) => {
    const followers = info.follower_count ?? 0;
    const likes = info.total_favorited ?? 0;
    return {
      handle: info.unique_id,
      name: info.nickname,
      followers,
      likes,
      videos: info.aweme_count ?? 0,
      verified: Boolean(info.custom_verify) || Boolean(info.enterprise_verify_reason),
      affinity: followers ? Number((likes / followers).toFixed(1)) : 0,
    };
  })
  .sort((a, b) => b.followers - a.followers);

console.error(`\nTikTok creators for "${keyword}":\n`);
console.error(
  "FOLLOWERS".padStart(11) + "  " + "LIKES".padStart(12) + "  " + "VIDEOS".padStart(6) + "  AFFINITY  HANDLE",
);
console.error("-".repeat(70));
for (const r of rows) {
  console.error(
    `${r.followers.toLocaleString().padStart(11)}  ${r.likes.toLocaleString().padStart(12)}  ` +
      `${String(r.videos).padStart(6)}  ${String(r.affinity).padStart(8)}  @${r.handle}${r.verified ? " [v]" : ""}`,
  );
}
console.log(JSON.stringify({ keyword, creators: rows }, null, 2));
