from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.domain.models.vehicle_position_model import VehiclePosition
from app.infrastructure.redis.connection import RedisConnection
from app.infrastructure.redis.tracking_repository import TrackingRepository

router = APIRouter(prefix="/tracking", tags=["Tracking"])


def get_repo():
    db = RedisConnection().get_client()
    return TrackingRepository(db)


# Update vehicle position
@router.post("/update")
def update_position(position: VehiclePosition, repo: TrackingRepository = Depends(get_repo)):
    repo.update_vehicle_position(position)
    return {"message": "Vehicle position updated"}


# Get current vehicle position
@router.get("/vehicle/{vehicle_id}")
def get_vehicle_position(vehicle_id: str, repo: TrackingRepository = Depends(get_repo)):
    data = repo.get_latest_position(vehicle_id)
    if not data:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return data


# Get last N positions
@router.get("/vehicle/{vehicle_id}/history")
def get_vehicle_history(vehicle_id: str, count: int = 10, repo: TrackingRepository = Depends(get_repo)):
    return repo.get_last_positions(vehicle_id, count)


# Get delay
@router.put("/delay/{trip_id}")
def update_delay(trip_id: str, delay_minutes: int, repo: TrackingRepository = Depends(get_repo)):
    repo.update_delay(trip_id, delay_minutes)
    return {"message": f"Trip {trip_id} delay updated to {delay_minutes} minutes"}

@router.put("/delay/{trip_id}")
def update_delay(trip_id: str, delay_minutes: int, repo: TrackingRepository = Depends(get_repo)):
    repo.update_delay(trip_id, delay_minutes)

    repo.publish_trip_update(trip_id, delay_minutes, "delayed")

    trip_line_id = "L1"  # < Mudar
    repo.publish_notification(trip_line_id, delay_minutes)

    return {"message": f"Trip {trip_id} delay updated and notification sent"}
