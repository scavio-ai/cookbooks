/**
 * shopping-route.ts -- a shopping-assistant API route (Next.js App Router).
 *
 * Drop this in as `app/api/shop/route.ts`. It exposes a POST endpoint that
 * takes { prompt } and returns a grounded shopping recommendation, comparing
 * live prices across Amazon and Walmart via the Scavio API. Works in any
 * Web-standard runtime (Next.js, Bun, Hono, Deno).
 *
 * It defines two compact tools directly on the `scavio` SDK -- extracting only
 * the fields the model needs (title, price, rating, reviews, url) -- because
 * raw retail search payloads are large. A clean pattern for building your own
 * AI SDK tools on top of Scavio.
 *
 * Setup (in your app):
 *   npm install ai @ai-sdk/openai scavio zod
 *   # env: SCAVIO_API_KEY, OPENAI_API_KEY
 *
 * Call it:
 *   curl -X POST localhost:3000/api/shop \
 *     -H 'content-type: application/json' \
 *     -d '{"prompt":"best value over-ear headphones under $200"}'
 */
import { generateText, stepCountIs, tool } from "ai";
import { openai } from "@ai-sdk/openai";
import { Scavio } from "scavio";
import { z } from "zod";

const scavio = new Scavio({ apiKey: process.env.SCAVIO_API_KEY });

function compact(products: any[], n = 8) {
  return (products ?? [])
    .filter((p) => !p.is_sponsored)
    .slice(0, n)
    .map((p) => ({
      title: p.title,
      price: p.price,
      currency: p.currency,
      rating: p.rating,
      reviews: p.reviews_count ?? p.rating_count,
      id: p.asin ?? p.id,
      url: p.url,
    }));
}

const amazonSearch = tool({
  description: "Search Amazon for products. Returns title, price, rating, reviews.",
  inputSchema: z.object({ query: z.string() }),
  execute: async ({ query }) => {
    const data = (await scavio.amazon.search({ query })).data as any;
    return compact(data?.products);
  },
});

const walmartSearch = tool({
  description: "Search Walmart for products. Returns title, price, rating, reviews.",
  inputSchema: z.object({ query: z.string() }),
  execute: async ({ query }) => {
    const data = (await scavio.walmart.search({ query })).data as any;
    return compact(data?.products);
  },
});

export async function POST(req: Request): Promise<Response> {
  const { prompt } = (await req.json()) as { prompt?: string };
  if (!prompt) {
    return Response.json({ error: "Missing 'prompt'." }, { status: 400 });
  }

  const { text } = await generateText({
    model: openai("gpt-4o"),
    tools: { amazon_search: amazonSearch, walmart_search: walmartSearch },
    stopWhen: stepCountIs(6),
    system:
      "You are a shopping assistant. Search BOTH Amazon and Walmart, compare " +
      "price, rating, and review count, and recommend the best pick plus one " +
      "runner-up. Always state where each item is cheaper and cite prices.",
    prompt,
  });

  return Response.json({ recommendation: text });
}
