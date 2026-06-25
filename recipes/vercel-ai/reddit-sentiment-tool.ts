/**
 * reddit-sentiment-tool.ts -- summarize Reddit sentiment for a brand/product.
 *
 * Hands the model the Scavio Reddit search tool and asks it to gauge how a
 * brand or product is talked about: overall sentiment, recurring praise, and
 * recurring complaints -- grounded in real, current threads.
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."
 *   export OPENAI_API_KEY="sk-..."
 *
 * Run:
 *   npm run reddit-sentiment -- "Rivian R1S"
 */
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";
import { scavioRedditSearch } from "@scavio/ai-sdk";

const subject = process.argv.slice(2).join(" ") || "Framework laptop";

const { text } = await generateText({
  model: openai("gpt-4o"),
  tools: {
    scavio_reddit_search: scavioRedditSearch({ apiKey: process.env.SCAVIO_API_KEY, maxResults: 10 }),
  },
  stopWhen: stepCountIs(4),
  system:
    "You analyze Reddit sentiment. Search a few query variations, then report: " +
    "1) overall sentiment (positive/mixed/negative), 2) top 3 praises, " +
    "3) top 3 complaints. Reference subreddits. Do not invent threads.",
  prompt: `What does Reddit think about: ${subject}?`,
});

console.log(`\nSentiment report -- ${subject}\n${"-".repeat(50)}\n${text}`);
