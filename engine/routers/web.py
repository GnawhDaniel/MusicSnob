from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db.database import SessionLocal
from internal.db.database import (
    youtube_get_all_channel_ids,
    get_latest_date,
    youtube_add_artist_data,
    get_db,
    youtube_get_deltas,
    youtube_check_duplicates,
    youtube_insert_artist
)
from internal.youtube.artist import getArtistsByChannelId
from internal.utils.utils import download_thumbnail
from engine.routers.auth import verify_session
from datetime import datetime
import logging
from typing import Annotated
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/web/v1")

db_dependency = Annotated[Session, Depends(get_db)]


class Artist(BaseModel):
    media_platform: str
    artist_id: str


def _do_daily_update():
    # Creating Session here because of CRON job in server.py
    # TODO: Consider parameter db=None and handle cases from server.py
    #       and daily_update endpoint. 
    db = SessionLocal()
    try:
        # Get all artists, then update stats for each artist.
        channel_ids = youtube_get_all_channel_ids(db)
        latest_date: str = get_latest_date(db)

        # Check if new day
        if datetime.now().strftime("%Y-%m-%d") <= latest_date.strftime("%Y-%m-%d"):
            logger.info("Skipping: already updated today")
            return

        # TODO: Bundle IDs into groups of 50 into Youtube API call (though API Youtube daily limit is 100,000)
        for channel_id in channel_ids:
            print("\n\n\n\n",channel_id)
            artist_info = getArtistsByChannelId(channel_id)
            subscribers = artist_info["items"][0]["statistics"]["subscriberCount"]
            total_views = artist_info["items"][0]["statistics"]["viewCount"]
            youtube_add_artist_data(db, channel_id, subscribers, total_views)
    finally:
        db.close()


@router.post("/artists/daily_update")
async def daily_update(db: db_dependency):
    # Get all artists, then update stats for each artist.

    latest_date: datetime = get_latest_date(db)

    # Check if new day
    if datetime.now().strftime("%Y-%m-%d") <= latest_date.strftime("%Y-%m-%d"):
        raise HTTPException(
            status_code=425, detail="Already pulled today's artists data."
        )

    _do_daily_update()


@router.get("/artists/deltas")
async def get_deltas(db: db_dependency):
    return youtube_get_deltas(db)


@router.get("/artist")
async def get_artist(youtube_channel_id: str, _is_valid_session = Depends(verify_session)):
    artist_info = getArtistsByChannelId(youtube_channel_id)
    return artist_info


@router.post("/artists/insert")
async def insert_artist(
    platform: Artist,
    db: db_dependency,
    _is_valid_session = Depends(verify_session),
):
    match platform.media_platform:
        case "youtube":
            youtube_channel_id = platform.artist_id

            if youtube_check_duplicates(db, youtube_channel_id):
                raise HTTPException(
                    status_code=400, detail="Artist already exists in database"
                )

            artist_info = getArtistsByChannelId(
                youtube_channel_id
            )  # TODO: Handle unknown channel IDs

            if artist_info["pageInfo"]["totalResults"] == 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Could not find channel id {youtube_channel_id}",
                )

            subscribers = artist_info["items"][0]["statistics"]["subscriberCount"]
            total_views = artist_info["items"][0]["statistics"]["viewCount"]
            name = artist_info["items"][0]["brandingSettings"]["channel"]["title"]
            thumbnail_url = artist_info["items"][0]["snippet"]["thumbnails"]["high"][
                "url"
            ]
            youtube_insert_artist(
                db, youtube_channel_id, subscribers, total_views, name
            )
            download_thumbnail(thumbnail_url, filename=f"{youtube_channel_id}.png")
        case _:
            raise HTTPException(status_code=400, detail="Unsupported media platform")
