from fastapi import APIRouter
from pydantic import BaseModel, Field

from internal.db.auth import get_user

router = APIRouter(prefix="/api/auth/v1")

class AuthenticationFields(BaseModel):
    username: str = Field(max_length=32)
    password: str = Field(description="Password must not exceed 64 chars" ,max_length=64)

@router.post("/sign-in")
def sign_in(auth_fields: AuthenticationFields):
    
    # Verify correct password
    get_user()

    # Create Session
    # Remove old session if applicable


    pass
