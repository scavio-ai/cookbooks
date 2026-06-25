/**
 * youtube-playlist-builder.ts -- search YouTube, build a ranked playlist JSON.
 *
 * Searches YouTube for a topic, sorts by view count, and emits a playlist
 * object (ordered video ids, titles, channels, watch URLs) ready to import,
 * embed, or hand to a "learn X from YouTube" UI.
 *
 * Setup:
 *   npm install
 *   export SCAVIO_API_KEY="sk_..."
 *
 * Run:
 *   npm run youtube-playlist -- "learn rust programming" 10
 */
import { Scavio } from "scavio";

const args = process.argv.slice(2);
const last = Number(args.at(-1));
const limit = Number.isNaN(last) ? 10 : last;
const topic = (Number.isNaN(last) ? args : args.slice(0, -1)).join(" ") || "learn rust programming";

const client = new Scavio({ apiKey: process.env.SCAVIO_API_KEY });
const res: any = await client.youtube.search({ query: topic, sort_by: "view_count", type: "video" });

const runs = (t: any) => (typeof t === "string" ? t : t?.runs?.[0]?.text ?? t?.simpleText ?? "");

const videos = (res.data?.results ?? [])
  .filter((v: any) => v.videoId)
  .slice(0, limit)
  .map((v: any, i: number) => ({
    position: i + 1,
    video_id: v.videoId,
    title: runs(v.title),
    channel: runs(v.ownerText) || runs(v.longBylineText),
    length: v.lengthText?.simpleText ?? runs(v.lengthText),
    url: `https://www.youtube.com/watch?v=${v.videoId}`,
  }));

const playlist = {
  title: `Playlist: ${topic}`,
  generated_at: new Date().toISOString(),
  count: videos.length,
  videos,
};

console.log(JSON.stringify(playlist, null, 2));
console.error(`Built a ${videos.length}-video playlist for "${topic}"`);
