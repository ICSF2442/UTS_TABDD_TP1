from fastapi import APIRouter, HTTPException, Depends
from app.domain.schemas.auth_schema import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token
from app.api.v1.users import FAKE_USERS_DB

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login_user(credentials: LoginRequest):
    # Find user by email
    user = next((u for u in FAKE_USERS_DB.values() if u.email == credentials.email), None)
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create token
    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)
