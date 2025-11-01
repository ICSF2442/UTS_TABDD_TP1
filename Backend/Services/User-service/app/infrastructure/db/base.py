from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from app.infrastructure.db.connection import Base

class UserDB(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class FavoriteDB(Base):
    __tablename__ = "favorites"

    favorite_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    line_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("UserDB", back_populates="favorites")


class FeedbackDB(Base):
    __tablename__ = "feedback"

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    rating = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("UserDB", back_populates="feedbacks")

class DriverDB(Base):
    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    contact = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("UserDB")

class NotificationDB(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    line_id = Column(Integer, nullable=True)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)
    sent_at = Column(DateTime, default=datetime.now)
    read = Column(Boolean, default=False)

    user = relationship("UserDB")

class ItineraryDB(Base):
    __tablename__ = "itineraries"

    itinerary_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    origin_id = Column(Integer, nullable=False)
    destination_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    expected_time = Column(DateTime, nullable=False)

    user = relationship("UserDB")

