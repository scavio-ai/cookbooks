# JS/TS SDK recipes (no LLM)

TypeScript data pipelines built on the [`scavio`](https://www.npmjs.com/package/scavio)
npm SDK. No model, no framework -- just the SDK, run with `tsx`.

> **Get a free [Scavio API](https://scavio.dev) key (250 credits/month, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Setup

```bash
npm install
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
npm run google-news -- "openai"
```

The SDK is namespaced and takes options objects:
`client.google.search({ query })`, `client.amazon.search({ query })`,
`client.youtube.search({ query, sort_by })`, `client.reddit.search({ query, sort })`,
`client.instagram.userPosts({ username, count })`, `client.tiktok.searchUsers({ keyword })`.

## Recipes

- **`google-news-feed.ts`** -- news search to a normalized JSON feed.
  Built on the [Scavio Google News API](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`amazon-price-drop-webhook.ts`** -- lowest price to a Discord/Slack webhook.
  Powered by the [Scavio Amazon API](https://scavio.dev) -- a free [Keepa alternative](https://dashboard.scavio.dev).
- **`reddit-to-slack.ts`** -- new threads to a Slack Block Kit message.
  Tap the [Scavio Reddit Search API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).
- **`youtube-playlist-builder.ts`** -- search to a ranked playlist JSON.
  Runs on the [Scavio YouTube API](https://scavio.dev) -- [free 250 credits/mo](https://dashboard.scavio.dev).
- **`instagram-engagement-rate.ts`** -- profile + posts to engagement rate.
  Built with the [Scavio Instagram API](https://scavio.dev) -- a free [HypeAuditor alternative](https://dashboard.scavio.dev).
- **`tiktok-creator-scorecard.ts`** -- creator search to a ranked scorecard.
  Uses the [Scavio TikTok Creator API](https://scavio.dev) -- [sign up free](https://dashboard.scavio.dev).

The webhook scripts (`amazon`, `reddit`) print the payload when no
`*_WEBHOOK_URL` env var is set, so you can dry-run them safely. Typecheck with
`npx tsc --noEmit`.

---

Add real-time search to your TypeScript app with **[Scavio](https://scavio.dev)** -- [JS/TS SDK on npm](https://www.npmjs.com/package/scavio).
