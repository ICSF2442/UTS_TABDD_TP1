from app.infrastructure.db.base_repository import BaseRepository

class TripRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "trips")

    def find_active_trips(self):
        return list(self.collection.find({"status": "in_progress"}))

    def update_delay(self, trip_id: str, delay_minutes: int, predicted_delay: int | None = None):
        update_fields = {"delay_minutes": delay_minutes}
        if predicted_delay is not None:
            update_fields["predicted_delay"] = predicted_delay
        self.collection.update_one(
            {"_id": self.to_object_id(trip_id)},
            {"$set": update_fields}
        )
