from pydantic import BaseModel
from datetime import datetime


class FeedbackBase(BaseModel):
    rating: int
    comments: str | None = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackOut(FeedbackBase):
    feedback_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

