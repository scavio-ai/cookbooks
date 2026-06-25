/**
 * google-news-feed.ts -- turn Google News results into a clean JSON feed.
 *
 * Queries the Scavio Google endpoint in "news" mode and emits a normalized
 * feed (title, source, url, date, snippet) you can render, cache, or push to
 * subscribers. A free alternative to the Google News API / SerpAPI news.
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev
 *
 * Run:
 *   npm run google-news -- "openai"
 *   npx tsx google-news-feed.ts "openai" > feed.json
 */
import { Scavio } from "scavio";

const query = process.argv.slice(2).join(" ") || "artificial intelligence";
const client = new Scavio({ apiKey: process.env.SCAVIO_API_KEY });

const res: any = await client.google.search({ query, search_type: "news" });
const items: any[] = res.news_results ?? res.top_stories ?? [];

const feed = {
  query,
  generated_at: new Date().toISOString(),
  count: items.length,
  items: items.map((n) => ({
    title: n.title,
    source: n.source,
    url: n.link,
    date: n.date ?? n.relative_date,
    snippet: n.snippet,
  })),
  credits_used: res.credits_used,
  credits_remaining: res.credits_remaining,
};

console.log(JSON.stringify(feed, null, 2));
console.error(`Built a ${feed.count}-item news feed for "${query}"`);
