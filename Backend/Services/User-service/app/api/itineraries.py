from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.connection import SessionLocal
from app.infrastructure.repositories.itinerary_repository import ItineraryRepository
from app.domain.schemas.itinerary_schema import ItineraryCreate, ItineraryOut
from app.domain.models.user import User
from app.api.users import get_current_user

router = APIRouter(prefix="/itineraries", tags=["Itineraries"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ItineraryOut)
def create_itinerary(payload: ItineraryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.user_id != payload.user_id:
        raise HTTPException(status_code=403, detail="Cannot create itineraries for other users")

    repo = ItineraryRepository(db)
    itin = repo.create_itinerary(payload.user_id, payload.origin_id, payload.destination_id, payload.start_time, payload.expected_time)
    return ItineraryOut(**itin.__dict__)


@router.get("/", response_model=list[ItineraryOut])
def get_user_itineraries(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ItineraryRepository(db)
    itineraries = repo.get_user_itineraries(current_user.user_id)
    return [ItineraryOut(**i.__dict__) for i in itineraries]


@router.delete("/{itinerary_id}")
def delete_itinerary(itinerary_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ItineraryRepository(db)
    itin = repo.find_by_id(itinerary_id)
    if not itin or itin.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    repo.delete_itinerary(itinerary_id)
    return {"message": f"Itinerary {itinerary_id} deleted successfully"}
