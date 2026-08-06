import pytest
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import text

from db.models import Users
from engine.routers.auth import AuthenticationFields, authenticate, verify_session
from internal.db.database import get_db
from internal.utils.auth import hash_password
from test.utils import (
    TestingSessionLocal,
    app,
    client,
    engine,
    override_get_db,
    override_verify_session_auth,
)


@pytest.fixture(autouse=True)
def dependency_overrides():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[verify_session] = override_verify_session_auth
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def generate_user():
    user = Users(user_id="test", hashed_pass=hash_password("test"))
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM Users;"))
        connection.commit()


def test_authenticate_valid(generate_user):
    db = TestingSessionLocal()
    auth_fields = AuthenticationFields(username="test", password="test")
    _user, _hashed_pass = authenticate(db, auth_fields)


def test_authenticate_invalid_password(generate_user):
    db = TestingSessionLocal()
    auth_fields = AuthenticationFields(username="test", password="tet")

    with pytest.raises(HTTPException) as exc:
        authenticate(db, auth_fields)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Wrong password"


def test_authenticate_invalid_user(generate_user):
    db = TestingSessionLocal()
    auth_fields = AuthenticationFields(username="tes", password="test")

    with pytest.raises(HTTPException) as exc:
        authenticate(db, auth_fields)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "Could not find user"


def test_sign_in_valid(generate_user):
    response = client.post(
        "/api/auth/v1/sign-in", json={"username": "test", "password": "test"}
    )
    client.cookies.clear()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Sign-in succesful"}


def test_sign_in_invalid(generate_user):
    response = client.post(
        "/api/auth/v1/sign-in", json={"username": "test", "password": "tst"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_artist_no_session():
    response = client.get(
        "/api/web/v1/artist?youtube_channel_id=UC0Q7Hlz75NYhYAuq6O0fqHw"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_artist_valid_session(generate_user):
    # Sign-in and receive auth cookie
    client.post("/api/auth/v1/sign-in", json={"username": "test", "password": "test"})
    response = client.get(
        "/api/web/v1/artist?youtube_channel_id=UC0Q7Hlz75NYhYAuq6O0fqHw"
    )
    client.cookies.clear()
    assert response.status_code == status.HTTP_200_OK
