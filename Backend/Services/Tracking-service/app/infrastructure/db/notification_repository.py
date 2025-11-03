from app.domain.models.notification import NotificationDB

class NotificationRepository:
    def __init__(self, db):
        self.db = db

    def save_notification(self, user_id: int, line_id: str, message: str, type: str):
        notif = NotificationDB(
            user_id=user_id,
            line_id=line_id,
            message=message,
            type=type
        )
        self.db.add(notif)
        self.db.commit()
        self.db.refresh(notif)
        return notif
