from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from internal.utils.utils import default_thumbnails_path

from .routers import auth, web

import db.models as models
from db.database import engine

import pytz


scheduler = BackgroundScheduler()


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

# Only creates new, if db/table does not exist
# Use alembic for any modifications to table columns
models.Base.metadata.create_all(bind=engine) 


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(web.router)
app.include_router(auth.router)