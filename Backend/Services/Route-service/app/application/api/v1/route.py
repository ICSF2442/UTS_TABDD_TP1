from fastapi import APIRouter, HTTPException, Depends
from app.infrastructure.db.connection import MongoDB
from app.infrastructure.db.line_repository import LineRepository
from app.infrastructure.db.stop_repository import StopRepository
from app.infrastructure.db.schedule_repository import ScheduleRepository
from app.infrastructure.db.trip_repository import TripRepository

router = APIRouter(prefix="/routes", tags=["Routes"])


# Dependency - connect to MongoDB
def get_db():
    return MongoDB()



# Stops
@router.get("/stops/{line_id}")
def get_stops_for_line(line_id: str, db: MongoDB = Depends(get_db)):
    repo = StopRepository(db)
    stops = repo.find_by_line_id(line_id)
    if not stops:
        raise HTTPException(status_code=404, detail="No stops found for this line")
    return {"line_id": line_id, "stops": stops}



# Lines
@router.get("/lines")
def get_all_lines(db: MongoDB = Depends(get_db)):
    repo = LineRepository(db)
    return repo.find_all()


@router.get("/lines/{line_id}")
def get_line_details(line_id: str, db: MongoDB = Depends(get_db)):
    line_repo = LineRepository(db)
    stop_repo = StopRepository(db)
    line = line_repo.find_by_id(line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found")

    stops = stop_repo.find_by_line_id(line_id)
    return {"line": line, "stops": stops}


#Schedules
@router.get("/schedules/{line_id}")
def get_schedules_for_line(line_id: str, db: MongoDB = Depends(get_db)):
    repo = ScheduleRepository(db)
    schedules = repo.find_by_line(line_id)
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found for this line")
    return {"line_id": line_id, "schedules": schedules}



#Trips
@router.get("/trips")
def get_all_trips(db: MongoDB = Depends(get_db)):
    repo = TripRepository(db)
    return repo.find_all()


@router.get("/trips/active")
def get_active_trips(db: MongoDB = Depends(get_db)):
    repo = TripRepository(db)
    return repo.find_active_trips()


@router.put("/trips/{trip_id}/delay")
def update_trip_delay(trip_id: str, delay_minutes: int, db: MongoDB = Depends(get_db)):
    repo = TripRepository(db)
    updated = repo.update_delay(trip_id, delay_minutes)
    if not updated:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message": f"Delay updated for trip {trip_id}"}
