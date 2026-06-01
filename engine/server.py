from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from internal.cfg.cfg import load_config
from internal.db.check_duplicates import youtube_check_duplicates
from internal.db.add_artist_data import youtube_add_artist_data
from internal.db.insert_artist import youtube_insert_artist
from internal.youtube.artist import getArtistsByChannelId
from internal.db.get_artist_deltas import youtube_get_deltas
from internal.db.get_artist import youtube_get_all_channel_ids

class Artist(BaseModel):
    media_platform: str
    artist_id: str

#example: UC39Q4fTGo8fW5ed9C6DSLuQ

cfg = load_config()

origins = ["http://localhost:5173"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/api/web/v1/artists/daily_update/")
def daily_update():
    # Bulk Get all artists, then update stats for each artist.
    
    channel_ids = youtube_get_all_channel_ids(cfg["DB_CONN"])
    
    # TODO: Bundle IDs into groups of 50 into Youtube API call 
    for channel_id in channel_ids:
        artist_info = getArtistsByChannelId(channel_id[0], cfg["YOUTUBE"]["API_URL"], cfg["YOUTUBE"]["API_KEY"])
        subscribers = artist_info["items"][0]["statistics"]["subscriberCount"]
        total_views = artist_info["items"][0]["statistics"]["viewCount"]
        youtube_add_artist_data(cfg["DB_CONN"], channel_id[0], subscribers, total_views)
    
    # youtube_add_artist_data(cfg["DB_CONN"])


@app.get("/api/web/v1/artists/deltas/")
def get_deltas():
    return youtube_get_deltas(cfg["DB_CONN"])


@app.post("/api/web/v1/artists/insert")
def insert_artist(platform: Artist):
    conn = cfg["DB_CONN"]
    
    match platform.media_platform:
        case "youtube":
            youtube_channel_id = platform.artist_id
            
            if (youtube_check_duplicates(conn, youtube_channel_id)):
                raise HTTPException(status_code=400, detail="Artist already exists in database")
            
            artist_info = getArtistsByChannelId(youtube_channel_id, cfg["YOUTUBE"]["API_URL"], cfg["YOUTUBE"]["API_KEY"])
            subscribers = artist_info["items"][0]["statistics"]["subscriberCount"]
            total_views = artist_info["items"][0]["statistics"]["viewCount"]
            name = artist_info["items"][0]["brandingSettings"]["channel"]["title"]
            print(artist_info)
            youtube_insert_artist(conn, youtube_channel_id, subscribers, total_views, name)
        case _:
            raise HTTPException(status_code=400, detail="Unsupported media platform")

