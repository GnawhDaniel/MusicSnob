"use server";

import { cookies } from "next/headers";
import { DeltaInterface } from "@/app/interfaces";

let apiBaseUrl = "http://server:5001";

export async function callAPI(endpoint: string, options?: RequestInit) {
  const res = await fetch(`${apiBaseUrl}${endpoint}`, options);
  if (!res.ok) {
    throw new Error(`API call failed with status ${res.status}`);
  }
  return res; // <-- return the Response itself, not res.json()
}

export async function getDeltas(): Promise<DeltaInterface[]> {
  const res = await callAPI("/api/web/v1/artists/deltas/");
  return res.json();
}

export async function addArtist(youtube_channel_id: string) {
  const res = await callAPI("/api/web/v1/artists/insert/", {
    method: "POST",
    body: JSON.stringify({
      media_platform: "youtube",
      artist_id: youtube_channel_id,
    }),
    headers: { "Content-Type": "application/json" },
  });
  return res.json();
}


export async function signIn(formData: FormData) {
  const username = formData.get("uname");
  const password = formData.get("passwd");

  const res = await callAPI("/api/auth/v1/sign-in/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
    headers: { "Content-Type": "application/json" },
  });


  // getSetCookie() returns string[] — one entry per Set-Cookie header
  const setCookies = res.headers.getSetCookie();
  const cookieStore = await cookies();

  for (const cookieStr of setCookies) {
    const parsed = parseSetCookie(cookieStr);
    cookieStore.set(parsed.name, parsed.value, parsed.options);
  }

  return res.json();
}

export async function getThumbnail(youtube_channel_id: string) {
  const res = await callAPI("/api/web/v1/thumbnail/", {
    method: "GET",
    body: JSON.stringify({
      media_platform: "youtube",
      artist_id: youtube_channel_id,
    }),
    headers: { "Content-Type": "application/json" },
  });
  return res.json();
}

// Minimal Set-Cookie string parser
function parseSetCookie(cookieStr: string) {
  const [pair, ...attrs] = cookieStr.split("; ");
  const [name, value] = pair.split("=");

  const options: Record<string, any> = {};
  for (const attr of attrs) {
    const [key, val] = attr.split("=");
    switch (key.toLowerCase()) {
      case "max-age":
        options.maxAge = Number(val);
        break;
      case "expires":
        options.expires = new Date(val);
        break;
      case "path":
        options.path = val;
        break;
      case "domain":
        options.domain = val;
        break;
      case "samesite":
        options.sameSite = val.toLowerCase();
        break;
      case "secure":
        options.secure = true;
        break;
      case "httponly":
        options.httpOnly = true;
        break;
    }
  }
  return { name, value, options };
}