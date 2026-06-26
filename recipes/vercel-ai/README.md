# Vercel AI SDK recipes

Tool-calling agents built with the [Vercel AI SDK](https://ai-sdk.dev) and
[`@scavio/ai-sdk`](https://www.npmjs.com/package/@scavio/ai-sdk), which wraps
the [Scavio API](https://scavio.dev) as ready-made AI SDK tools.

> **Get a free Scavio API key (50 free credits, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
npm install
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
npm run research -- "What shipped in the latest Next.js release?"
```

`scavioTools({ apiKey, maxResults })` returns all seven tools keyed by name
(`scavio_search`, `scavio_amazon_search`, `scavio_instagram_search`, ...), or
import a single factory like `scavioSearch()` / `scavioRedditSearch()`.

## Recipes

- **`research-stream.ts`** -- streamed, cited research answer.
  Grounded by the [Scavio web search API](https://scavio.dev) -- a free [Tavily alternative](https://dashboard.scavio.dev).
- **`reddit-sentiment-tool.ts`** -- brand/product sentiment report.
  Powered by the [Scavio Reddit Search API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`instagram-influencer-vet.ts`** -- creator discovery + vetting.
  Built with the [Scavio Instagram API](https://scavio.dev) -- a free [Modash alternative](https://dashboard.scavio.dev).
- **`shopping-route.ts`** -- a Next.js App Router shopping endpoint.
  Compares live prices via the [Scavio Amazon + Walmart APIs](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).

`shopping-route.ts` is a Web-standard `POST` handler -- drop it in at
`app/api/shop/route.ts` (Next.js) or serve it from Bun/Hono/Deno unchanged.
Multi-step tool loops use `stopWhen: stepCountIs(n)` (AI SDK v5+).

---

Give your Vercel AI SDK agents real-time search with **[Scavio](https://scavio.dev)** -- [@scavio/ai-sdk on npm](https://www.npmjs.com/package/@scavio/ai-sdk).
