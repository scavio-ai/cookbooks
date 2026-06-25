/**
 * instagram-influencer-vet.ts -- vet Instagram creators for a campaign.
 *
 * Gives the model the Scavio Instagram search tool and asks it to find and
 * vet creators for a niche -- surfacing handles, apparent focus, and fit for a
 * given brief. A free starting point for influencer discovery (Modash, Heepsy).
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."
 *   export OPENAI_API_KEY="sk-..."
 *
 * Run:
 *   npm run instagram-vet -- "sustainable home goods for a small DTC brand"
 */
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";
import { scavioInstagramSearch } from "@scavio/ai-sdk";

const brief =
  process.argv.slice(2).join(" ") || "specialty coffee creators for a roaster's launch";

const { text } = await generateText({
  model: openai("gpt-4o"),
  tools: {
    scavio_instagram_search: scavioInstagramSearch({
      apiKey: process.env.SCAVIO_API_KEY,
      maxResults: 12,
    }),
  },
  stopWhen: stepCountIs(4),
  system:
    "You are an influencer-marketing scout. Search Instagram for creators and " +
    "hashtags matching the brief, then return a shortlist of 5 handles with a " +
    "one-line fit rationale each. Only list handles that appeared in results.",
  prompt: `Find Instagram creators for this campaign brief: ${brief}`,
});

console.log(`\nInfluencer shortlist\nBrief: ${brief}\n${"-".repeat(50)}\n${text}`);
