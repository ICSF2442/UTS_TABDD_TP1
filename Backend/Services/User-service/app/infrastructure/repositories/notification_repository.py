from sqlalchemy.orm import Session
from app.infrastructure.db.base import NotificationDB

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def send_notification(self, user_id: int, message: str, type: str, line_id: int | None = None):
        notif = NotificationDB(user_id=user_id, message=message, type=type, line_id=line_id)
        self.db.add(notif)
        self.db.commit()
        self.db.refresh(notif)
        return notif

    def get_user_notifications(self, user_id: int):
        return self.db.query(NotificationDB).filter(NotificationDB.user_id == user_id).all()

    def mark_as_read(self, notification_id: int):
        notif = self.db.query(NotificationDB).filter(NotificationDB.notification_id == notification_id).first()
        if notif:
            notif.read = True
            self.db.commit()
        return notif
