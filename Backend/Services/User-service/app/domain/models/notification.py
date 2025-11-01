from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    line_id = Column(Integer, nullable=True)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)
    sent_at = Column(DateTime, default=datetime.now)
    read = Column(Boolean, default=False)

    user = relationship("User")
