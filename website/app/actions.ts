"use server";

import { cookies } from "next/headers";
import { DeltaInterface } from "@/app/interfaces";
import { redirect } from "next/navigation";

let apiBaseUrl = "http://server:5001";

export async function callAPI(endpoint: string, options?: RequestInit) {
  const cookieStore = await cookies();
  const cookieHeader = cookieStore
    .getAll()
    .map((c) => `${c.name}=${c.value}`)
    .join("; ");

  const res = await fetch(`${apiBaseUrl}${endpoint}`, {
    ...options,
    headers: {
      ...options?.headers,
      Cookie: cookieHeader,
    },
  });

  if (!res.ok) {
    throw new Error(`API call failed with status ${res.status}`);
  }
  return res;
}

export async function getDeltas(): Promise<DeltaInterface[]> {
  const res = await callAPI("/api/web/v1/artists/deltas/");
  return res.json();
}

export async function addArtist(formData: FormData) {
  const youtube_channel_id = formData.get("youtube_channel_id");

  let res;
  try {
    res = await callAPI("/api/web/v1/artists/insert/", {
      method: "POST",
      body: JSON.stringify({
        media_platform: "youtube",
        artist_id: youtube_channel_id,
      }),
      headers: { "Content-Type": "application/json" },
    });
  } catch (e) {
    redirect("/sign-in");
  }

  // return res.json();
  return redirect("/"); // Refresh page to see added artist
}

export async function deleteArtist(youtube_channel_id: string) {
  try {
    const res = await callAPI("/api/web/v1/artists/delete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        media_platform: "youtube",
        artist_id: youtube_channel_id,
      }),
    });

    if (!res.ok) {
      throw new Error(`Request failed: ${res.status}`);
    }
  } catch (err) {}
  console.log("Deleted successfully");
  return redirect("/");
}

export async function signIn(formData: FormData) {
  const username = formData.get("uname");
  const password = formData.get("passwd");

  let res;

  try {
    res = await callAPI("/api/auth/v1/sign-in/", {
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
  } catch (e) {
    // TODO: Handle errors (invalid credentials, 5xx, etc.)
  }

  redirect("/");
}

export async function getArtistInfo(youtube_channel_id: string) {
  try {
    const res = await callAPI(
      `/api/web/v1/artists/get?youtube_channel_id=${youtube_channel_id}`,
      {
        method: "GET",
      },
    );

    if (res.status == 404) {
      return null;
    }

    return res.json();
  } catch (e) {
    console.log(e);
  }
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
