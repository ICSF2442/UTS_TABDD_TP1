from pydantic import BaseModel
from datetime import datetime


class DriverBase(BaseModel):
    name: str
    license_number: str
    contact: str | None = None


class DriverCreate(DriverBase):
    user_id: int


class DriverOut(DriverBase):
    driver_id: int
    user_id: int
    active: bool
    created_at: datetime

    class Config:
        orm_mode = True