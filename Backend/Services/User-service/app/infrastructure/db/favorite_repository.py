from sqlalchemy.orm import Session
from app.infrastructure.db.base import FavoriteDB


class FavoriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_favorite(self, user_id: int, line_id: int):
        favorite = FavoriteDB(user_id=user_id, line_id=line_id)
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def remove_favorite(self, user_id: int, line_id: int):
        fav = self.db.query(FavoriteDB).filter(
            FavoriteDB.user_id == user_id, FavoriteDB.line_id == line_id
        ).first()
        if fav:
            self.db.delete(fav)
            self.db.commit()
        return fav

    def get_favorites(self, user_id: int):
        return self.db.query(FavoriteDB).filter(FavoriteDB.user_id == user_id).all()
