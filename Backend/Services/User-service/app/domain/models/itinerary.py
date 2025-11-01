from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base


class Itinerary(Base):
    __tablename__ = "itineraries"

    itinerary_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    origin_id = Column(Integer, nullable=False)
    destination_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    expected_time = Column(DateTime, nullable=False)

    user = relationship("User")
