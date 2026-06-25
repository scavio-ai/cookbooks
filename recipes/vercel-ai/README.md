# Vercel AI SDK recipes

Tool-calling agents built with the [Vercel AI SDK](https://ai-sdk.dev) and
[`@scavio/ai-sdk`](https://www.npmjs.com/package/@scavio/ai-sdk), which wraps
the Scavio API as ready-made AI SDK tools.

## Setup

```bash
npm install
export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev
export OPENAI_API_KEY="sk-..."
npm run research -- "What shipped in the latest Next.js release?"
```

`scavioTools({ apiKey, maxResults })` returns all seven tools keyed by name
(`scavio_search`, `scavio_amazon_search`, `scavio_instagram_search`, ...), or
import a single factory like `scavioSearch()` / `scavioRedditSearch()`.

## Recipes

| File | What it does | Tools |
|---|---|---|
| `research-stream.ts` | Streamed, cited research answer | Google |
| `reddit-sentiment-tool.ts` | Brand/product sentiment report | Reddit |
| `instagram-influencer-vet.ts` | Creator discovery + vetting | Instagram |
| `shopping-route.ts` | Next.js App Router shopping endpoint | Amazon + Walmart |

`shopping-route.ts` is a Web-standard `POST` handler -- drop it in at
`app/api/shop/route.ts` (Next.js) or serve it from Bun/Hono/Deno unchanged.

Multi-step tool loops use `stopWhen: stepCountIs(n)` (AI SDK v5+). Typecheck
with `npx tsc --noEmit`.
