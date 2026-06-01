# Gets all artists, consider pulling only "n" artist at a time
def youtube_get_deltas(conn):
    cursor = conn.cursor()

    # TODO: Very Likely Candidate for Optimization
    # Domain Expansion: Cursed SQL query
    res = cursor.execute("""
        SELECT youtube_artists.youtube_channel_id, 
            artist_name, 
            latest_subscriber_count-min(subscriber_count) as subscriber_delta, 
            max(view_count)-min(view_count) as view_delta, 
            min(view_count) as min_view_count,
            latest_subscriber_count,
            earliest_subscriber_count
        FROM youtube_artist_stats
        
        JOIN youtube_artists ON youtube_artist_stats.youtube_id = youtube_artists.youtube_id
        
        JOIN (
            SELECT youtube_id,
                MAX(CASE WHEN rn_asc  = 1 THEN subscriber_count END) AS earliest_subscriber_count,
                MAX(CASE WHEN rn_desc = 1 THEN subscriber_count END) AS latest_subscriber_count
            FROM (
                SELECT
                    youtube_id,
                    subscriber_count,
                    ROW_NUMBER() OVER (PARTITION BY youtube_id ORDER BY date_pulled ASC)  AS rn_asc,
                    ROW_NUMBER() OVER (PARTITION BY youtube_id ORDER BY date_pulled DESC) AS rn_desc
                FROM youtube_artist_stats
                )
            GROUP BY youtube_id) AS c 
        ON youtube_artist_stats.youtube_id = c.youtube_id
                
        GROUP BY youtube_artists.youtube_channel_id
        
        """).fetchall()

    for i, delta in enumerate(res):
        temp_dict = dict()
        temp_dict["channel_id"] = delta[0]
        temp_dict["artist_name"] = delta[1]
        temp_dict["subs_delta"] = delta[2]
        temp_dict["views_delta"] = delta[3]
        temp_dict["min_view_count"] = delta[4]
        temp_dict["latest_sub_count"] = delta[5]
        temp_dict["earliest_sub_count"] = delta[6]
        res[i] = temp_dict

    return res
