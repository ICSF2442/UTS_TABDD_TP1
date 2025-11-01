from pydantic import BaseModel
from datetime import datetime


class NotificationBase(BaseModel):
    message: str
    type: str
    line_id: int | None = None


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationOut(NotificationBase):
    notification_id: int
    user_id: int
    sent_at: datetime
    read: bool

    class Config:
        orm_mode = True