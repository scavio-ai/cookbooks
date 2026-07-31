/**
 * amazon-price-drop-webhook.ts -- ping a webhook when an Amazon item is cheap.
 *
 * Searches Amazon for a product, finds the lowest-priced organic match, and
 * fires a Discord/Slack-style webhook when it is at or below your target
 * price. No webhook set? It prints the alert instead, so you can test dry.
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."
 *   export PRICE_WEBHOOK_URL="https://discord.com/api/webhooks/..."   # optional
 *
 * Run:
 *   npm run amazon-webhook -- "sony wh-1000xm5" 300
 */
import { Scavio } from "scavio";

const args = process.argv.slice(2);
const target = Number(args.at(-1));
const hasTarget = !Number.isNaN(target);
const query = (hasTarget ? args.slice(0, -1) : args).join(" ") || "sony wh-1000xm5";
const threshold = hasTarget ? target : 300;

const client = new Scavio({ apiKey: process.env.SCAVIO_API_KEY });
// Amazon results are unsorted and cannot be sorted upstream, so the cheapest
// listing is picked client-side below.
const res: any = await client.amazon.search({ query });

const cheapest = (res.data?.products ?? [])
  .filter((p: any) => !p.is_sponsored && typeof p.price === "number" && p.price > 0)
  .sort((a: any, b: any) => a.price - b.price)[0];

if (!cheapest) {
  console.error(`No priced results for "${query}".`);
  process.exit(0);
}

console.error(`Cheapest "${query}": $${cheapest.price} (target $${threshold})`);

if (cheapest.price <= threshold) {
  const text =
    `Price drop: ${cheapest.title}\n` +
    `$${cheapest.price} (<= $${threshold})  rating ${cheapest.rating ?? "n/a"}\n` +
    `https://www.amazon.com/dp/${cheapest.asin}`;

  const url = process.env.PRICE_WEBHOOK_URL;
  if (url) {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: text }), // Discord shape; Slack uses { text }
    });
    console.error("Webhook fired.");
  } else {
    console.log("[would POST to PRICE_WEBHOOK_URL]\n" + text);
  }
} else {
  console.error("Above target -- no alert.");
}
