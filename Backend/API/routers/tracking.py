from fastapi import APIRouter
from services.redis_client import RedisClient

router = APIRouter(prefix="/tracking", tags=["Tracking"])
redis_client = RedisClient()

@router.get("/vehicles")
def get_latest_vehicle_positions():
    entries = redis_client.read_latest_updates(count=10)
    parsed = []
    for entry in entries:
        data = entry[1].get("data")
        if data:
            parsed.append(data)
    return {"vehicles": parsed}
