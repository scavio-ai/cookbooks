/**
 * research-stream.ts -- a grounded research answer streamed token-by-token.
 *
 * Gives the model the Scavio Google search tool and streams a cited answer to
 * any question, using live web results instead of stale training data. The
 * canonical "search-grounded chatbot" loop in ~30 lines.
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."        # https://dashboard.scavio.dev
 *   export OPENAI_API_KEY="sk-..."
 *
 * Run:
 *   npm run research -- "What shipped in the latest Next.js release?"
 */
import { streamText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";
import { scavioSearch } from "@scavio/ai-sdk";

const question =
  process.argv.slice(2).join(" ") || "What are the most-discussed AI coding tools right now?";

const result = streamText({
  model: openai("gpt-4o"),
  tools: { scavio_search: scavioSearch({ apiKey: process.env.SCAVIO_API_KEY, maxResults: 6 }) },
  stopWhen: stepCountIs(5),
  system:
    "You are a research assistant. Use the scavio_search tool to find current " +
    "information before answering. Cite source URLs inline as [n] and list them at the end.",
  prompt: question,
});

process.stdout.write(`\nQ: ${question}\n\n`);
for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
process.stdout.write("\n");
