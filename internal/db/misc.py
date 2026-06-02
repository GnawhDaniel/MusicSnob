
def get_latest_date(conn):
    cursor = conn.cursor()
    
    res = cursor.execute("""
                         
                         SELECT MAX(date_pulled)
                         FROM youtube_artist_stats
                         
                         """).fetchone()
    
    return res[0]
    