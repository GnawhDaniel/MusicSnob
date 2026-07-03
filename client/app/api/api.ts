export interface DeltaInterface {
  channel_id: string;
  artist_name: string;
  subs_delta: number;
  views_delta: number;
  min_view_count: number;
  latest_sub_count: number;
  earliest_sub_count: number;
  subscription_date: string;
}

async function callApi(endpoint: string, options?: RequestInit) {
  let apiBaseUrl =
    typeof window === "undefined"
      ? (process.env.API_BASE_URL ?? "http://localhost:5001")
      : (import.meta.env.VITE_API_BASE_URL ??
        "http://localhost:5001");

  console.log(typeof window);
  console.log(apiBaseUrl);
  const res = await fetch(`${apiBaseUrl}${endpoint}`, options);
  if (!res.ok) {
    throw new Error(`API call failed with status ${res.status}`);
  }
  return res.json();
}

export async function getDeltas(): Promise<DeltaInterface[]> {
  return callApi("/api/web/v1/artists/deltas/");
}

export async function addArtist(youtube_channel_id: string) {
  const options = {
    method: "POST",
    body: JSON.stringify({
      media_platform: "youtube",
      artist_id: youtube_channel_id,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  };
  return callApi("/api/web/v1/artists/insert/", options);
}

export async function getThumbnail(youtube_channel_id: string) {
  const options = {
    method: "GET",
    body: JSON.stringify({
      media_platform: "youtube",
      artist_id: youtube_channel_id,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  };
  return callApi("/api/web/v1/thumbnail/", options);
}


export async function signIn(username: string, password: string) {
    const options = {
    method: "POST",
    body: JSON.stringify({
      username: username,
      password: password,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  };
  return callApi("/api/auth/v1/sign-in/", options);

}