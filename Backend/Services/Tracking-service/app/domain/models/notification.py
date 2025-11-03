from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from app.infrastructure.db.base_class import Base

class NotificationDB(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    line_id = Column(String(50))
    message = Column(Text)
    type = Column(String(50))
    sent_at = Column(DateTime, default=datetime.utcnow)
