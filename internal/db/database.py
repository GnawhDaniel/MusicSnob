from fastapi import HTTPException
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import YouTubeArtistStats, YouTubeArtists, Artists
import datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def youtube_check_duplicates(db, youtube_channel_id: str) -> bool:
    count = (
        db.query(func.count(YouTubeArtists.youtube_id))
        .filter(YouTubeArtists.youtube_channel_id == youtube_channel_id)
        .scalar()
    )

    return count > 0


def get_latest_date(db):
    return db.query(func.max(YouTubeArtistStats.date_pulled)).scalar()


def youtube_get_all_channel_ids(db: Session):
    stmt = select(YouTubeArtists.youtube_channel_id)
    return db.execute(stmt).scalars().all()


def youtube_add_artist_data(
    db: Session,
    youtube_channel_id: str,
    subscribers: int,
    total_views: int,
):
    # Get youtube_id from youtube_artists table
    stmt = select(YouTubeArtists.youtube_id).where(
        YouTubeArtists.youtube_channel_id == youtube_channel_id
    )
    youtube_id = db.execute(stmt).scalar_one()

    stats = YouTubeArtistStats(
        youtube_id=youtube_id,
        subscriber_count=subscribers,
        view_count=total_views,
        date_pulled=datetime.datetime.today(),
    )
    db.add(stats)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()  # row for this youtube_id + date already exists — ignore, matches OR IGNORE


def youtube_insert_artist(
    db: Session,
    youtube_channel_id: str,
    subscribers: int,
    total_views: int,
    name: str,
):
    # TODO: implement ability to manually merge artists;
    # probably by repointing artist_id from youtube_artists to desired artists id.

    try:
        # Create new entry in artists table
        artist = Artists(name=name)
        db.add(artist)

        # Create new entry in youtube_artists table
        yt_artist = YouTubeArtists(
            youtube_channel_id=youtube_channel_id,
            artist_name=name,
        )
        db.add(yt_artist)
        db.flush()  # populates yt_artist.youtube_id via the autoincrement

        # Create the stats row, setting the FK explicitly
        stats = YouTubeArtistStats(
            youtube_id=yt_artist.youtube_id,
            subscriber_count=subscribers,
            view_count=total_views,
            date_pulled=datetime.datetime.today(),
        )
        db.add(stats)

        db.commit()
    except IntegrityError:
        db.rollback()
        raise  # or handle duplicate channel_id gracefully here


def youtube_get_artist(db: Session, youtube_channel_id: str):
    yt_artist = (
        db.query(YouTubeArtists)
        .filter(YouTubeArtists.youtube_channel_id == youtube_channel_id)
        .first()
    )
    
    if yt_artist is None:
        raise HTTPException(status_code=404, detail="YouTube artist not found")

    return yt_artist

def youtube_delete_artist(db: Session, youtube_channel_id: str):
    try:
        yt_artist = (
            db.query(YouTubeArtists)
            .filter(YouTubeArtists.youtube_channel_id == youtube_channel_id)
            .first()
        )

        if yt_artist is None:
            raise HTTPException(status_code=404, detail="YouTube artist not found")

        artist = db.query(Artists).filter(Artists.name == yt_artist.artist_name).first()

        if artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")

        db.delete(artist)
        db.delete(yt_artist)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise


# Gets all artists, consider pulling only "n" artist at a time
def youtube_get_deltas(db):

    # TODO: Very Likely Candidate for Optimization
    # Domain Expansion: Cursed SQL query
    query = text("""
        SELECT youtube_artists.youtube_channel_id, 
            artist_name, 
            latest_subscriber_count-min(subscriber_count) as subscriber_delta, 
            max(view_count)-min(view_count) as view_delta, 
            min(view_count) as min_view_count,
            latest_subscriber_count,
            earliest_subscriber_count,
            min(date_pulled) as sub_date
        FROM youtube_artist_stats
        
        JOIN youtube_artists ON youtube_artist_stats.youtube_id = youtube_artists.youtube_id
        
        JOIN (
            SELECT youtube_id,
                MAX(CASE WHEN rn_asc  = 1 THEN subscriber_count END) AS earliest_subscriber_count,
                MAX(CASE WHEN rn_desc = 1 THEN subscriber_count END) AS latest_subscriber_count
            FROM (
                SELECT
                    youtube_id,
                    subscriber_count,
                    ROW_NUMBER() OVER (PARTITION BY youtube_id ORDER BY date_pulled ASC)  AS rn_asc,
                    ROW_NUMBER() OVER (PARTITION BY youtube_id ORDER BY date_pulled DESC) AS rn_desc
                FROM youtube_artist_stats
                )
            GROUP BY youtube_id) AS c 
        ON youtube_artist_stats.youtube_id = c.youtube_id
                
        GROUP BY youtube_artists.youtube_channel_id
        
        """)

    return db.execute(query).mappings().all()
