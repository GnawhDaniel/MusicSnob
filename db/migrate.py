import sqlite3

OLD_DB = "data.db"
NEW_DB = "data2.db"

def migrate():
    old_conn = sqlite3.connect(OLD_DB)
    new_conn = sqlite3.connect(NEW_DB)

    old_conn.execute("PRAGMA foreign_keys=OFF")  # allow bulk insert in any order
    new_conn.execute("PRAGMA foreign_keys=OFF")

    old_cur = old_conn.cursor()
    new_cur = new_conn.cursor()

    # --- artists ---
    old_cur.execute("SELECT id, name FROM artists")
    artists = old_cur.fetchall()
    new_cur.executemany("INSERT INTO artists (id, name) VALUES (?, ?)", artists)
    print(f"Migrated {len(artists)} rows into artists")

    # --- youtube_artists ---
    old_cur.execute("SELECT youtube_id, youtube_channel_id, artist_name FROM youtube_artists")
    yt_artists = old_cur.fetchall()
    new_cur.executemany(
        "INSERT INTO youtube_artists (youtube_id, youtube_channel_id, artist_name) VALUES (?, ?, ?)",
        yt_artists,
    )
    print(f"Migrated {len(yt_artists)} rows into youtube_artists")

    # --- youtube_artist_stats ---
    old_cur.execute("SELECT youtube_id, date_pulled, subscriber_count, view_count FROM youtube_artist_stats")
    stats = old_cur.fetchall()
    new_cur.executemany(
        "INSERT INTO youtube_artist_stats (youtube_id, date_pulled, subscriber_count, view_count) VALUES (?, ?, ?, ?)",
        stats,
    )
    print(f"Migrated {len(stats)} rows into youtube_artist_stats")

    new_conn.commit()

    new_conn.execute("PRAGMA foreign_keys=ON")

    old_conn.close()
    new_conn.close()
    print("Migration complete.")


if __name__ == "__main__":
    migrate()