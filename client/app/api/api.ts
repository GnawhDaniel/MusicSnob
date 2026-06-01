export interface DeltaInterface {
  youtube_channel_id: string;
  artist_name: string;
  subs_delta: number;
  views_delta: number;
  min_view_count: number;
  latest_sub_count: number;
  earliest_sub_count: number
}

export const apiBaseUrl = "http://localhost:8000/api/web/v1";

async function callApi(endpoint: string, options?: RequestInit) {
  const res = await fetch(`${apiBaseUrl}${endpoint}`, options);
  if (!res.ok) {
    throw new Error(`API call failed with status ${res.status}`);
  }
  return res.json();
}

export async function getDeltas(): Promise<DeltaInterface[]> {
  return callApi("/artists/deltas/");
}

export async function addArtist(youtube_channel_id: string) {
  const options = {
    method: "POST",
    body: JSON.stringify({ media_platform: "youtube", artist_id: youtube_channel_id }),
    headers: {
      "Content-Type": "application/json",
    },
  };
  return callApi("/artists/insert/", options);
}
