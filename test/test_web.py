from datetime import datetime, timedelta

import pytest
from fastapi import status
from sqlalchemy import text

from db.models import Artists, YouTubeArtists, YouTubeArtistStats
from engine.routers.auth import verify_session
from internal.db.database import get_db
from test.utils import (
    TestingSessionLocal,
    app,
    client,
    engine,
    override_get_db,
    override_verify_session_noauth,
)


@pytest.fixture(autouse=True)
def dependency_overrides():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[verify_session] = override_verify_session_noauth
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def test_update():
    artist = YouTubeArtists(
        youtube_id=1,
        youtube_channel_id="UC0Q7Hlz75NYhYAuq6O0fqHw",
        artist_name="Jeremy's IT Lab",
    )
    artist_stat_1 = YouTubeArtistStats(
        youtube_id=1,
        date_pulled=datetime.now() - timedelta(days=2),
        subscriber_count=100,
        view_count=10_000,
    )

    db = TestingSessionLocal()
    db.add(artist)
    db.commit()
    db.add(artist_stat_1)
    db.commit()
    yield
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM youtube_artists;"))
        connection.execute(text("DELETE FROM youtube_artist_stats;"))
        connection.commit()


@pytest.fixture
def test_deltas():
    yt_artist = YouTubeArtists(
        youtube_id=1, youtube_channel_id="testchannelid", artist_name="test"
    )

    artist_stat_1 = YouTubeArtistStats(
        youtube_id=1,
        date_pulled=datetime.now() - timedelta(days=1),
        subscriber_count=100,
        view_count=10_000,
    )
    artist_stat_2 = YouTubeArtistStats(
        youtube_id=1,
        date_pulled=datetime.now(),
        subscriber_count=1_000,
        view_count=100_000,
    )

    db = TestingSessionLocal()
    db.add(yt_artist)
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


# TODO: _daily_update hard codes session which prevents pytest from using sessionlocal
# def test_daily_update(test_update):
#     response = client.post("/api/web/v1/artists/daily_update")

# # Should have 2 rows
# sess = TestingSessionLocal()
# res = sess.execute(select(YouTubeArtistStats)).all()
# print(res)
# sess.close()
# assert len(res) == 2
# assert response.status_code == status.HTTP_200_OK


def test_daily_update_fail(test_deltas):
    response = client.post("/api/web/v1/artists/daily_update")
    assert response.status_code == status.HTTP_425_TOO_EARLY
    assert response.json() == {"detail": "Already pulled today's artists data."}


def test_insert_artist_valid(test_deltas):
    response = client.post(
        "/api/web/v1/artists/insert",
        json={"media_platform": "youtube", "artist_id": "UC0Q7Hlz75NYhYAuq6O0fqHw"},
    )
    assert response.status_code == status.HTTP_200_OK


def test_insert_artist_duplicate_artist(test_deltas):
    client.post(
        "/api/web/v1/artists/insert",
        json={"media_platform": "youtube", "artist_id": "UC0Q7Hlz75NYhYAuq6O0fqHw"},
    )
    response = client.post(
        "/api/web/v1/artists/insert",
        json={"media_platform": "youtube", "artist_id": "UC0Q7Hlz75NYhYAuq6O0fqHw"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Artist already exists in database"}


def test_insert_artist_invalid_channel_id():
    response = client.post(
        "/api/web/v1/artists/insert",
        json={"media_platform": "youtube", "artist_id": "invalid"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": 'Could not find channel id "invalid"'}


def test_insert_artist_invalid_platform():
    response = client.post(
        "/api/web/v1/artists/insert",
        json={"media_platform": "tiktok", "artist_id": ""},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Unsupported media platform"}


def test_get_artist_invalid():
    response = client.get(
        "/api/web/v1/artists/get?youtube_channel_id=notarealchannelid"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_artist_valid(test_deltas):
    response = client.get("/api/web/v1/artists/get?youtube_channel_id=testchannelid")
    assert response.json() == {
        "youtube_id": 1,
        "youtube_channel_id": "testchannelid",
        "artist_name": "test",
    }
    assert response.status_code == status.HTTP_200_OK


def test_delete_artist_valid(test_deltas):
    response = client.post(
        "/api/web/v1/artists/delete",
        json={"media_platform": "youtube", "artist_id": "testchannelid"},
    )
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    try:
        rows = db.query(YouTubeArtists).all()
        assert len(rows) == 0, f"Expected no rows, but got {len(rows)}"
    finally:
        db.close()


def test_delete_artist_invalid(test_deltas):
    response = client.post(
        "/api/web/v1/artists/delete",
        json={"media_platform": "youtube", "artist_id": "nonexistant"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "YouTube artist not found"}

    db = TestingSessionLocal()
    try:
        rows = db.query(YouTubeArtists).all()
        assert len(rows) == 1, f"Expected 1 rows, but got {len(rows)}"
    finally:
        db.close()