/**
 * reddit-to-slack.ts -- post new Reddit threads for a keyword to Slack.
 *
 * Searches Reddit "new" for a keyword and sends the latest threads as a Slack
 * message (Block Kit). No webhook configured? It prints the payload so you can
 * see exactly what would be sent. Free alternative to F5Bot + Zapier.
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."
 *   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."   # optional
 *
 * Run:
 *   npm run reddit-slack -- "serpapi alternative"
 */
import { Scavio } from "scavio";

const query = process.argv.slice(2).join(" ") || "serpapi alternative";
const client = new Scavio({ apiKey: process.env.SCAVIO_API_KEY });

const res: any = await client.reddit.search({ query, sort: "new" });
const posts: any[] = (res.data?.posts ?? []).slice(0, 5);

const lines = posts.map(
  (p) => `*<${p.url}|${p.title}>*\nr/${p.subreddit} - u/${p.author}`,
);

const payload = {
  text: `New Reddit threads for "${query}"`,
  blocks: [
    { type: "header", text: { type: "plain_text", text: `Reddit: ${query}` } },
    ...lines.map((l) => ({ type: "section", text: { type: "mrkdwn", text: l } })),
  ],
};

const url = process.env.SLACK_WEBHOOK_URL;
if (url) {
  await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  console.error(`Posted ${posts.length} threads to Slack.`);
} else {
  console.log(JSON.stringify(payload, null, 2));
  console.error(`[would POST ${posts.length} threads to SLACK_WEBHOOK_URL]`);
}
