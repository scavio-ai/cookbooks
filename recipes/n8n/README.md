# n8n recipes

Importable [n8n](https://n8n.io) workflows that use the
[`n8n-nodes-scavio`](https://www.npmjs.com/package/n8n-nodes-scavio) community
node -- no code, just a scheduled automation.

## Setup

1. In n8n: **Settings -> Community Nodes -> Install** `n8n-nodes-scavio`.
2. Add a **Scavio API** credential with your key (https://dashboard.scavio.dev).
3. **Import from File** one of the JSON workflows below.
4. Map the Scavio credential, fill in the placeholders (Slack webhook / SMTP /
   target price), and activate.

> **Get a free Scavio API key (50 free credits, no card): [dashboard.scavio.dev](https://dashboard.scavio.dev)**

## Workflows

- **`reddit-mention-to-slack.json`** -- hourly Reddit keyword search to a Slack
  webhook. Powered by the [Scavio Reddit Search API](https://scavio.dev) -- a free
  [F5Bot alternative](https://dashboard.scavio.dev).
- **`amazon-price-drop-email.json`** -- daily Amazon price check, emails you when
  it drops below target. Built on the [Scavio Amazon API](https://scavio.dev) --
  [get a free key](https://dashboard.scavio.dev).

The Scavio node is `Resource` + `Operation` driven (Google, Amazon, Walmart,
YouTube, Reddit, TikTok, Instagram, Account), so you can swap in any other
Scavio endpoint by changing those two dropdowns.

---

Automate real-time search in n8n with **[Scavio](https://scavio.dev)** -- [n8n-nodes-scavio on npm](https://www.npmjs.com/package/n8n-nodes-scavio).
