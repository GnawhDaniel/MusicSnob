def youtube_get_all_channel_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT youtube_channel_id FROM youtube_artists")
    return cursor.fetchall()
