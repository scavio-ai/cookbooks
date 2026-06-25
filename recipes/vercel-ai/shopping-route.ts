/**
 * shopping-route.ts -- a shopping-assistant API route (Next.js App Router).
 *
 * Drop this in as `app/api/shop/route.ts`. It exposes a POST endpoint that
 * takes { prompt } and returns a grounded shopping recommendation, using the
 * Scavio Amazon + Walmart search tools to compare live prices across both
 * retailers. Works in any Web-standard runtime (Next.js, Bun, Hono, Deno).
 *
 * Setup (in your app):
 *   npm install ai @ai-sdk/openai @scavio/ai-sdk zod
 *   # env: SCAVIO_API_KEY, OPENAI_API_KEY
 *
 * Call it:
 *   curl -X POST localhost:3000/api/shop \
 *     -H 'content-type: application/json' \
 *     -d '{"prompt":"best value over-ear headphones under $200"}'
 */
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";
import { scavioAmazonSearch, scavioWalmartSearch } from "@scavio/ai-sdk";

export async function POST(req: Request): Promise<Response> {
  const { prompt } = (await req.json()) as { prompt?: string };
  if (!prompt) {
    return Response.json({ error: "Missing 'prompt'." }, { status: 400 });
  }

  const cfg = { apiKey: process.env.SCAVIO_API_KEY, maxResults: 8 };

  const { text } = await generateText({
    model: openai("gpt-4o"),
    tools: {
      scavio_amazon_search: scavioAmazonSearch(cfg),
      scavio_walmart_search: scavioWalmartSearch(cfg),
    },
    stopWhen: stepCountIs(6),
    system:
      "You are a shopping assistant. Search BOTH Amazon and Walmart, compare " +
      "price, rating, and review count, and recommend the best pick plus one " +
      "runner-up. Always state where each item is cheaper and cite prices.",
    prompt,
  });

  return Response.json({ recommendation: text });
}
