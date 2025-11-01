from sqlalchemy.orm import Session
from app.infrastructure.db.base import ItineraryDB

class ItineraryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_itinerary(self, user_id: int, origin_id: int, destination_id: int, start_time, expected_time):
        itin = ItineraryDB(
            user_id=user_id,
            origin_id=origin_id,
            destination_id=destination_id,
            start_time=start_time,
            expected_time=expected_time
        )
        self.db.add(itin)
        self.db.commit()
        self.db.refresh(itin)
        return itin

    def get_user_itineraries(self, user_id: int):
        return self.db.query(ItineraryDB).filter(ItineraryDB.user_id == user_id).all()

    def find_by_id(self, itinerary_id: int):
        return self.db.query(ItineraryDB).filter(ItineraryDB.itinerary_id == itinerary_id).first()

    def delete_itinerary(self, itinerary_id: int):
        itin = self.find_by_id(itinerary_id)
        if itin:
            self.db.delete(itin)
            self.db.commit()
        return itin
