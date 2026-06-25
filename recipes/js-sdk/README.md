# JS/TS SDK recipes (no LLM)

TypeScript data pipelines built on the [`scavio`](https://www.npmjs.com/package/scavio)
npm SDK. No model, no framework -- just the SDK, run with `tsx`.

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

| Script | What it does | Platform |
|---|---|---|
| `google-news-feed.ts` | News search -> normalized JSON feed | Google |
| `amazon-price-drop-webhook.ts` | Lowest price -> Discord/Slack webhook | Amazon |
| `reddit-to-slack.ts` | New threads -> Slack Block Kit message | Reddit |
| `youtube-playlist-builder.ts` | Search -> ranked playlist JSON | YouTube |
| `instagram-engagement-rate.ts` | Profile + posts -> engagement rate | Instagram |
| `tiktok-creator-scorecard.ts` | Creator search -> ranked scorecard | TikTok |

The webhook scripts (`amazon`, `reddit`) print the payload when no
`*_WEBHOOK_URL` env var is set, so you can dry-run them safely.

Typecheck everything with `npx tsc --noEmit`.
