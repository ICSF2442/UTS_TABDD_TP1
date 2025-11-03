from app.infrastructure.db.base_repository import BaseRepository

class LineRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "lines")
