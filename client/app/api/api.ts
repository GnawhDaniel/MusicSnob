export interface DeltaInterface {
  artist_name: string;
  min_subscriber_count: number;
  min_view_count: number;
  subscriber_delta: number;
  view_delta: number;
  youtube_channel_id: string;
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
