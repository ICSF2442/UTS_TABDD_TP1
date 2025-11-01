# app/api/v1/users.py
from fastapi import APIRouter, HTTPException, Depends, Header
from datetime import datetime
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.domain.schemas.user_schema import UserCreate, UserOut, UserUpdate
from app.domain.models.user import User
from app.core.security import hash_password
from app.core.config import settings
from app.infrastructure.db.connection import SessionLocal
from app.infrastructure.db.user_repository import UserRepository
from app.infrastructure.db.favorite_repository import FavoriteRepository
from app.infrastructure.db.feedback_repository import FeedbackRepository
from app.domain.schemas.feedback_schema import (
    FeedbackCreate,
    FeedbackOut,
)
from app.domain.schemas.favorite_schema import (
    FavoriteCreate,
    FavoriteOut
)



router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------- AUTH ----------------------
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    # VALIDAÇAO DO JWT
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        repo = UserRepository(db)
        user = repo.find_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")
        return current_user
    return role_checker


# ---------------------- CRUD ----------------------

@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    # Check for existing user
    if repo.find_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create and save user
    hashed_pw = hash_password(payload.password)
    user = User(None, payload.name, payload.email, hashed_pw, payload.role)
    user = repo.save(user)
    return UserOut(**user.__dict__)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = UserRepository(db)
    user = repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user.__dict__)


@router.get("/all", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    repo = UserRepository(db)
    users = repo.find_all()
    return [UserOut(**u.__dict__) for u in users]


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = UserRepository(db)
    user = repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Only allow self or admin
    if current_user.user_id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only edit your own profile")

    # Apply changes
    if payload.name:
        user.name = payload.name
    if payload.email:
        user.email = payload.email
    if payload.password:
        user.password_hash = hash_password(payload.password)

    repo.update(user)
    return UserOut(**user.__dict__)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = UserRepository(db)
    user = repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.user_id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only delete your own account")

    repo.delete(user)
    return {"message": "User deleted successfully"}


# ---------- Favorites ----------
@router.post("/{user_id}/favorites", response_model=FavoriteOut)
def add_favorite(
    user_id: int,
    payload: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot modify another user's favorites")

    repo = FavoriteRepository(db)
    fav = repo.add_favorite(user_id, payload.line_id)
    return FavoriteOut(
        favorite_id=fav.favorite_id,
        line_id=fav.line_id,
        created_at=fav.created_at
    )


@router.get("/{user_id}/favorites", response_model=list[FavoriteOut])
def get_favorites(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot view another user's favorites")

    repo = FavoriteRepository(db)
    favs = repo.get_favorites(user_id)
    return [
        FavoriteOut(
            favorite_id=f.favorite_id,
            line_id=f.line_id,
            created_at=f.created_at
        )
        for f in favs
    ]


@router.delete("/{user_id}/favorites/{line_id}")
def remove_favorite(
    user_id: int,
    line_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot modify another user's favorites")

    repo = FavoriteRepository(db)
    deleted = repo.remove_favorite(user_id, line_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Favorite not found")

    return {"message": f"Line {line_id} removed from favorites"}


# ---------- Feedback ----------
@router.post("/{user_id}/feedback", response_model=FeedbackOut)
def add_feedback(
    user_id: int,
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot submit feedback for another user")

    repo = FeedbackRepository(db)
    fb = repo.add_feedback(user_id, payload.rating, payload.comments)
    return FeedbackOut(
        feedback_id=fb.feedback_id,
        user_id=fb.user_id,
        rating=fb.rating,
        comments=fb.comments,
        created_at=fb.created_at
    )


@router.get("/{user_id}/feedback", response_model=list[FeedbackOut])
def get_feedback(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    repo = FeedbackRepository(db)
    feedbacks = repo.get_feedback_by_user(user_id)
    return [
        FeedbackOut(
            feedback_id=f.feedback_id,
            user_id=f.user_id,
            rating=f.rating,
            comments=f.comments,
            created_at=f.created_at
        )
        for f in feedbacks
    ]




