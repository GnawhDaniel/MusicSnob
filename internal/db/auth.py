from hashlib import sha256
from datetime import datetime, timedelta
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from db.models import AuthSessions, Users


def get_user(db: Session, username: str):
    stmt = select(Users.user_id, Users.hashed_pass).where(Users.user_id == username)
    return db.execute(stmt).first()


def insert_session(db: Session, session_id, username):
    sha256_sessionid = sha256(session_id.encode("utf-8")).hexdigest()
    created_at = datetime.now()
    expiry = created_at + timedelta(days=1)

    session = AuthSessions(
        session_id=sha256_sessionid,
        user_id=username,
        created_at=created_at,
        expiry=expiry,
    )
    db.add(session)
    db.commit()


def remove_session_by_user(db: Session, username: str):
    stmt = delete(AuthSessions).where(AuthSessions.user_id == username)
    db.execute(stmt)
    db.commit()


def is_session(db: Session, session_id) -> bool:
    hashed_id = sha256(session_id.encode("utf-8")).hexdigest()
    
    session = db.get(AuthSessions, hashed_id)
    
    if not session:
        return False

    # Check token expiry
    if datetime.now() > session.expiry:
        return False

    return True
