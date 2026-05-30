import datetime


def youtube_insert_artist(conn, youtube_channel_id, subscribers, total_views, name):
    cursor = conn.cursor()
    # TODO: implement ability to manually merge artists;
    # probably by repointing artist_id from youtube_artists to desired artists id.
    print(name)
    # Create new entry in artists table
    cursor.execute("INSERT INTO artists(name) VALUES (?)", (name,))

    cursor.execute(
        "INSERT INTO youtube_artists(youtube_channel_id, artist_name) VALUES (?, ?)",
        (youtube_channel_id, name),
    )

    # Get youtube_id from youtube_artists table
    r = cursor.execute(
        "SELECT youtube_id FROM youtube_artists WHERE youtube_channel_id = ?",
        (youtube_channel_id,),
    )
    youtube_id = r.fetchone()[0]

    cursor.execute(
        "INSERT INTO youtube_artist_stats(youtube_id, subscriber_count, view_count, date_pulled) VALUES (?, ?, ?, ?)",
        (
            youtube_id,
            subscribers,
            total_views,
            datetime.datetime.today().strftime("%Y-%m-%d"),
        ),
    )
    conn.commit()
