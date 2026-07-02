from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from internal.db.auth import get_user, insert_session, remove_session_by_user
from internal.cfg.cfg import cfg

from internal.utils.auth import verify_hash, generate_session_id

router = APIRouter(prefix="/api/auth/v1")

class AuthenticationFields(BaseModel):
    username: str = Field(max_length=32)
    password: str = Field(description="Password must not exceed 64 chars" ,max_length=64)


def authenticate(auth_fields: AuthenticationFields):
    user = get_user(cfg["AUTH_CONN"], auth_fields.username)
    if not user:
        raise HTTPException(status_code=404, detail=f"Could not find user {auth_fields.username}")
    username, hashed_pass = user

    if not verify_hash(hashed_pass, auth_fields.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    return user


@router.post("/sign-in")
def sign_in(auth_fields: AuthenticationFields):
        
    # Verify correct password (authentication)
    username, _ = authenticate(auth_fields)

    # Create Session
    # ------------------------------------------
    # Generate Session ID
    session_id = generate_session_id()

    # Remove old session if applicable
    remove_session_by_user(cfg["AUTH_CONN"], username)

    # Insert Session ID to table
    insert_session(cfg["AUTH_CONN"], session_id, username)


    # Return Cookie with Session ID
    response = JSONResponse(status_code=200, content={"detail": "success"})
    response.set_cookie(
        key="__Host-SessionID", 
        value=session_id, 
        secure=True, 
        httponly= True,
        samesite='strict',
        )
    return response




