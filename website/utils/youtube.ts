import "server-only";
import * as cheerio from "cheerio";

export async function getYouTubeChannelID(url: string) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const html = await response.text();
  const $ = cheerio.load(html);

  const canonicalUrl = $('link[rel="canonical"]').attr("href");

  if (!canonicalUrl) {
    return null;
  }

  const match = canonicalUrl.match(
    /youtube\.com\/channel\/([^/?#]+)/
  );

  return match?.[1] ?? null;
}