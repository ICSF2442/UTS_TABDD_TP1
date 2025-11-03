from app.infrastructure.db.base_repository import BaseRepository

class StopRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "stops")

    def find_by_line_id(self, line_id: str):
        return list(self.collection.find({"line_id": line_id}).sort("order", 1))
