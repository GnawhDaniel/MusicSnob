def youtube_check_duplicates(conn, youtube_channel_id):
    cursor = conn.cursor()
    
    params = (youtube_channel_id,)
    
    cursor.execute(
        "SELECT COUNT(*) FROM youtube_artists WHERE youtube_channel_id = ?", 
        params
    )
    
    count = cursor.fetchone()[0]
    
    return count > 0