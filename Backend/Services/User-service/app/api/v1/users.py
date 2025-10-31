# app/api/v1/users.py
from fastapi import APIRouter, HTTPException, Depends, Header
from datetime import datetime
from jose import JWTError, jwt
from app.domain.schemas.user_schema import UserCreate, UserOut
from app.domain.models.user import User
from app.core.security import hash_password
from app.core.config import settings

router = APIRouter(prefix="/users", tags=["Users"])

FAKE_USERS_DB: dict[int, User] = {} # !!!! Alterar mais tarde 31/10
COUNTER = 1

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("sub")
        user = next((u for u in FAKE_USERS_DB.values() if u.email == email), None)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate):
    global COUNTER
    for u in FAKE_USERS_DB.values():
        if u.email == payload.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(payload.password)
    new_user = User(user_id=COUNTER, name=payload.name, email=payload.email, password_hash=hashed)
    FAKE_USERS_DB[COUNTER] = new_user
    COUNTER += 1

    return UserOut(**new_user.__dict__)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    user = FAKE_USERS_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user.__dict__)
