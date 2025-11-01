from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.connection import SessionLocal
from app.infrastructure.db.notification_repository import NotificationRepository
from app.domain.schemas.notification_schema import NotificationCreate, NotificationOut
from app.domain.models.user import User
from app.api.v1.users import get_current_user, require_role

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=NotificationOut)
def send_notification(payload: NotificationCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    repo = NotificationRepository(db)
    notif = repo.send_notification(payload.user_id, payload.message, payload.type, payload.line_id)
    return NotificationOut(**notif.__dict__)


@router.get("/", response_model=list[NotificationOut])
def get_user_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = NotificationRepository(db)
    notifs = repo.get_user_notifications(current_user.user_id)
    return [NotificationOut(**n.__dict__) for n in notifs]


@router.patch("/{notification_id}/read", response_model=NotificationOut)
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = NotificationRepository(db)
    notif = repo.mark_as_read(notification_id)
    if not notif or notif.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationOut(**notif.__dict__)
