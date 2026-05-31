# Gets all artists, consider pulling only "n" artist at a time
def youtube_get_deltas(conn):
    cursor = conn.cursor()
    res = cursor.execute("""
        SELECT youtube_artists.youtube_channel_id, 
            artist_name, 
            max(subscriber_count)-min(subscriber_count) as subscriber_delta, 
            max(view_count)-min(view_count) as view_delta, 
            min(subscriber_count) as min_subscriber_count,
            min(view_count) as min_view_count
        FROM youtube_artist_stats
        JOIN youtube_artists ON youtube_artist_stats.youtube_id = youtube_artists.youtube_id
        GROUP BY youtube_artists.youtube_channel_id
        
        """).fetchall()

    for i, delta in enumerate(res):
        temp_dict = dict()
        temp_dict["youtube_channel_id"] = delta[0]
        temp_dict["artist_name"] = delta[1]
        temp_dict["subscriber_delta"] = delta[2]
        temp_dict["view_delta"] = delta[3]
        temp_dict["min_subscriber_count"] = delta[4]
        temp_dict["min_view_count"] = delta[5]
        res[i] = temp_dict

    return res
