from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from db.database import SessionLocal
from internal.db.auth import (
    get_user,
    insert_session,
    remove_session_by_user,
    is_session,
)
from internal.db.database import get_db
from internal.utils.auth import verify_hash, generate_session_id

router = APIRouter(prefix="/api/auth/v1")
db_dependency = Annotated[Session, Depends(get_db)]


class AuthenticationFields(BaseModel):
    username: str = Field(max_length=32)
    password: str = Field(
        description="Password must not exceed 64 chars", max_length=64
    )


def authenticate(db: Session, auth_fields: AuthenticationFields):
    user = get_user(db, auth_fields.username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"Could not find user {auth_fields.username}"
        )
    _username, hashed_pass = user

    if not verify_hash(hashed_pass, auth_fields.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    return user


def verify_session(request: Request) -> bool:
    db = SessionLocal()
    try:
        session = request.cookies.get("__Host-SessionID")
        if not session or not is_session(db, session):
            raise HTTPException(status_code=404, detail="Invalid session")
    finally:
        db.close()

@router.post("/sign-in")
def sign_in(auth_fields: AuthenticationFields, db: db_dependency):

    # Verify correct password (authentication)
    username, _ = authenticate(db, auth_fields)
    # Create Session
    # ------------------------------------------
    # Generate Session ID
    session_id = generate_session_id()

    # Remove old session if applicable
    remove_session_by_user(db, username)

    # Insert Session ID to table
    insert_session(db, session_id, username)

    # Return Cookie with Session ID
    response = JSONResponse(status_code=200, content={"detail": "success"})
    response.set_cookie(
        key="__Host-SessionID",
        value=session_id,
        secure=True,
        httponly=True,
        samesite="lax",
    )
    return response
