from pydantic import BaseModel
from datetime import datetime

class FavoriteBase(BaseModel):
    line_id: int


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteOut(FavoriteBase):
    favorite_id: int
    created_at: datetime

    class Config:
        orm_mode = True