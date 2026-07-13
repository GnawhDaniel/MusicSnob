from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, text
from engine.routers.auth import verify_session
import engine.server
from internal.db.database import get_db
from db.models import Base, YouTubeArtistStats, YouTubeArtists
import pytest
from datetime import datetime, timedelta

app = engine.server.app
SQL_ALCHEMY_DATABASE_URL = "sqlite:///./db/testdb.db"
engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# ==================== Overrides ====================
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_verify_session():
    return


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[verify_session] = override_verify_session


# ==================== TESTS ====================
client = TestClient(app)


@pytest.fixture
def test_deltas():
    artist = YouTubeArtists(
        youtube_id=1,
        youtube_channel_id="testchannelid",
        artist_name="test"
    )
    
    artist_stat_1 = YouTubeArtistStats(
        youtube_id=1,
        date_pulled=datetime.now() - timedelta(days=1),
        subscriber_count=100,
        view_count=10_000
    )
    artist_stat_2 = YouTubeArtistStats(
        youtube_id=1,
        date_pulled=datetime.now(),
        subscriber_count=1000,
        view_count=100_000
    )
    
    db = TestingSessionLocal()
    db.add(artist)
    db.commit()
    db.add(artist_stat_1)
    db.commit()
    db.add(artist_stat_2)
    db.commit()
    yield 
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM youtube_artists;"))
        connection.execute(text("DELETE FROM youtube_artist_stats;"))
        connection.commit()


def test_return_health():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}


def test_get_artist():
    # Invalid channel id
    response = client.get("/api/web/v1/artist?youtube_channel_id=null")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["pageInfo"]["totalResults"] == 0

    # Valid channel
    # Jeremy's IT Lab: UC0Q7Hlz75NYhYAuq6O0fqHw
    response = client.get(
        "/api/web/v1/artist?youtube_channel_id=UC0Q7Hlz75NYhYAuq6O0fqHw"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["pageInfo"]["totalResults"] == 1


def test_get_deltas(test_deltas):
    response = client.get("/api/web/v1/artists/deltas")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    views = data[0]["view_delta"]  
    subs = data[0]["subscriber_delta"]
    assert views == 90_000
    assert subs == 900