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