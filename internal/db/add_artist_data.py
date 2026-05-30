import datetime

def youtube_add_artist_data(conn, youtube_channel_id, subscribers, total_views):
    cursor = conn.cursor()
    
    # Get youtube_id from youtube_artists table
    r = cursor.execute("SELECT youtube_id FROM youtube_artists WHERE youtube_channel_id = ?", (youtube_channel_id, ))
    youtube_id = r.fetchone()[0]

    cursor.execute(
        "INSERT OR IGNORE INTO youtube_artist_stats(youtube_id, subscriber_count, view_count, date_pulled) VALUES (?, ?, ?, ?)", 
        (youtube_id, subscribers, total_views, datetime.datetime.today().strftime("%Y-%m-%d"))
    )
    conn.commit()