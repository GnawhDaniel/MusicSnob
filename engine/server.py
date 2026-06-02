from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from internal.cfg.cfg import load_config
from internal.db.check_duplicates import youtube_check_duplicates
from internal.db.add_artist_data import youtube_add_artist_data
from internal.db.insert_artist import youtube_insert_artist
from internal.db.get_artist_deltas import youtube_get_deltas
from internal.db.get_artist import youtube_get_all_channel_ids
from internal.db.misc import get_latest_date
from internal.youtube.artist import getArtistsByChannelId
from internal.utils.utils import download_thumbnail, download_youtube_missing_thumbnails
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("apscheduler").setLevel(logging.DEBUG)

cfg = load_config()
scheduler = BackgroundScheduler()


class Artist(BaseModel):
    media_platform: str
    artist_id: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(
        _do_daily_update,
        "cron",
        hour=0,
        minute=5,
        timezone=pytz.timezone("America/Chicago"),
    )
    scheduler.start()
    yield
    scheduler.shutdown()


origins = [
    "http://localhost:5173",
    "http://web:5000",
    "http://localhost:8000",
    "http://localhost:5000",
]


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter(prefix="/api/web/v1")


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
def insert_artist(platform: Artist):
    conn = cfg["DB_CONN"]

    match platform.media_platform:
        case "youtube":
            youtube_channel_id = platform.artist_id

            if youtube_check_duplicates(conn, youtube_channel_id):
                raise HTTPException(
                    status_code=400, detail="Artist already exists in database"
                )

            artist_info = getArtistsByChannelId(youtube_channel_id)
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


@app.get("/utils/_download_youtube_missing_thumbnails")
def get_youtube_missing_thumbnails():
    return download_youtube_missing_thumbnails(cfg["DB_CONN"])


app.include_router(router)
