from app.infrastructure.db.base_repository import BaseRepository

class ScheduleRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "schedules")

    def find_by_line(self, line_id: str):
        return list(self.collection.find({"line_id": line_id}))
