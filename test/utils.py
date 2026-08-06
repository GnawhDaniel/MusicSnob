from fastapi import HTTPException, Request
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import engine.server
from db.models import Base
from engine.routers.auth import is_session

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


def override_verify_session_auth(request: Request):
    db = TestingSessionLocal()
    try:
        session = request.cookies.get("__Host-SessionID")
        if not session or not is_session(db, session):
            raise HTTPException(status_code=404, detail="Invalid session")
    finally:
        db.close()


def override_verify_session_noauth():
    return


client = TestClient(app, base_url="https://testserver")
