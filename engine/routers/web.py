from fastapi import APIRouter, HTTPException, APIRouter, Depends
from pydantic import BaseModel

from internal.db.check_duplicates import youtube_check_duplicates
from internal.db.add_artist_data import youtube_add_artist_data
from internal.db.insert_artist import youtube_insert_artist
from internal.db.get_artist_deltas import youtube_get_deltas
from internal.db.get_artist import youtube_get_all_channel_ids
from internal.db.misc import get_latest_date
from internal.youtube.artist import getArtistsByChannelId
from internal.utils.utils import download_thumbnail

from internal.cfg.cfg import cfg

from engine.routers.auth import verify_session

from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/web/v1")

class Artist(BaseModel):
    media_platform: str
    artist_id: str

def _do_daily_update():
    # Get all artists, then update stats for each artist.
    channel_ids = youtube_get_all_channel_ids(cfg["DB_CONN"])
    latest_date: str = get_latest_date(cfg["DB_CONN"])

    # Check if new day
    if datetime.now().strftime("%Y-%m-%d") <= latest_date:
        logger.info("Skipping: already updated today")
        return

    # TODO: Bundle IDs into groups of 50 into Youtube API call (though API Youtube daily limit is 100,000)
    for channel_id in channel_ids:
        artist_info = getArtistsByChannelId(channel_id[0])
        subscribers = artist_info["items"][0]["statistics"]["subscriberCount"]
        total_views = artist_info["items"][0]["statistics"]["viewCount"]
        youtube_add_artist_data(cfg["DB_CONN"], channel_id[0], subscribers, total_views)

@router.post("/artists/daily_update")
def daily_update():
    # Get all artists, then update stats for each artist.

    latest_date: str = get_latest_date(cfg["DB_CONN"])
    print(latest_date)

    # Check if new day
    if datetime.now().strftime("%Y-%m-%d") <= latest_date:
        raise HTTPException(
            status_code=425, detail="Already pulled today's artists data."
        )

    _do_daily_update()


@router.get("/artists/deltas")
def get_deltas():
    return youtube_get_deltas(cfg["DB_CONN"])


@router.get("/artist/")
def get_artist(youtube_channel_id: str):
    artist_info = getArtistsByChannelId(youtube_channel_id)
    return artist_info


@router.post("/artists/insert")
def insert_artist(platform: Artist, is_valid_session: bool = Depends(verify_session)):
    if not is_valid_session:
        # TODO: Redirect
        print("Not valid")
        return
    
    conn = cfg["DB_CONN"]

    match platform.media_platform:
        case "youtube":
            youtube_channel_id = platform.artist_id

            if youtube_check_duplicates(conn, youtube_channel_id):
                raise HTTPException(
                    status_code=400, detail="Artist already exists in database"
                )

            artist_info = getArtistsByChannelId(youtube_channel_id) #TODO: Handle unknown channel IDs
            subscribers = artist_info["items"][0]["statistics"]["subscriberCount"]
            total_views = artist_info["items"][0]["statistics"]["viewCount"]
            name = artist_info["items"][0]["brandingSettings"]["channel"]["title"]
            thumbnail_url = artist_info["items"][0]["snippet"]["thumbnails"]["high"][
                "url"
            ]
            youtube_insert_artist(
                conn, youtube_channel_id, subscribers, total_views, name
            )
            download_thumbnail(thumbnail_url, filename=f"{youtube_channel_id}.png")
        case _:
            raise HTTPException(status_code=400, detail="Unsupported media platform")