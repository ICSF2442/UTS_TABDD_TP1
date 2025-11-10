from fastapi import APIRouter, Body, HTTPException
from datetime import datetime
from app.infrastructure.redis.tracking_repository import TrackingRepository
from app.domain.models.vehicle_position_model import VehiclePosition

router = APIRouter(prefix="/tracking", tags=["Tracking"])

repo = TrackingRepository()

@router.post("/update")
def receive_vehicle_position(data: dict = Body(...)):
    """
    Recebe posicao.
    """
    try:
        ts_str = data["timestamp"].replace("Z", "")
        position = VehiclePosition(
            vehicle_id=data["vehicle_id"],
            line_id=data["line_id"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            speed=data.get("speed", 0.0),
            timestamp=datetime.fromisoformat(ts_str),
        )

        repo.update_vehicle_position(position)

        return {
            "status": "ok",
            "stored": True,
            "vehicle_id": position.vehicle_id,
            "timestamp": position.timestamp.isoformat()
        }

    except Exception as e:
        print("Error while processing position:", e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/latest/{vehicle_id}")
def get_latest(vehicle_id: int):
    """
    Returns the last known position of a vehicle.
    """
    result = repo.get_latest_position(vehicle_id)
    if not result:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return result


@router.get("/history/{vehicle_id}")
def get_history(vehicle_id: int, count: int = 10):
    """
    Returns the last N positions for replay or analysis.
    """
    return repo.get_last_positions(vehicle_id, count)
