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

## Workflows

| File | What it does | Platform |
|---|---|---|
| `reddit-mention-to-slack.json` | Hourly Reddit keyword search -> Slack webhook | Reddit |
| `amazon-price-drop-email.json` | Daily Amazon price check -> email when below target | Amazon |

The Scavio node is `Resource` + `Operation` driven (Google, Amazon, Walmart,
YouTube, Reddit, TikTok, Instagram, Account), so you can swap in any other
Scavio endpoint by changing those two dropdowns.
