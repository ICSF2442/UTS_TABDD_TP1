from pydantic import BaseModel
from datetime import datetime

class ItineraryBase(BaseModel):
    origin_id: int
    destination_id: int
    start_time: datetime
    expected_time: datetime


class ItineraryCreate(ItineraryBase):
    user_id: int


class ItineraryOut(ItineraryBase):
    itinerary_id: int
    user_id: int

    class Config:
        orm_mode = True