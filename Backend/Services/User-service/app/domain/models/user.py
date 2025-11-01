from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.infrastructure.db.base import Base  # make sure Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User {self.user_id}: {self.email} ({self.role})>"
