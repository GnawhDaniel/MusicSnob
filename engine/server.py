from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from internal.cfg.cfg import cfg, load_config
from internal.utils.utils import default_thumbnails_path

from .routers import auth, web

import pytz
import logging

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("apscheduler").setLevel(logging.DEBUG)


scheduler = BackgroundScheduler()

load_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(
        web._do_daily_update,
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

app.mount("/api/web/v1/thumbnail", StaticFiles(directory=default_thumbnails_path), name="thumbnail")


# @app.get("/utils/_download_youtube_missing_thumbnails")
# def get_youtube_missing_thumbnails():
#     return download_youtube_missing_thumbnails(cfg["DB_CONN"])


app.include_router(web.router)
app.include_router(auth.router)