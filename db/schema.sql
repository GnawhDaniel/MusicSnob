CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS youtube_artists (
    youtube_id INTEGER PRIMARY KEY AUTOINCREMENT,
    youtube_channel_id TEXT NOT NULL UNIQUE,
    artist_name TEXT
);

CREATE TABLE IF NOT EXISTS youtube_artist_stats (
    youtube_id INTEGER NOT NULL,
    date_pulled TEXT NOT NULL,
    subscriber_count INTEGER NOT NULL,
    view_count INTEGER NOT NULL,
    PRIMARY KEY (youtube_id, date_pulled),
    FOREIGN KEY (youtube_id) REFERENCES youtube_artists(youtube_id) ON DELETE CASCADE
)