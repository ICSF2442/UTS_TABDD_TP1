from fastapi import APIRouter
from datetime import datetime
import random
from services.redis_client import RedisClient

router = APIRouter(prefix="/mock", tags=["Vehicle Mock"])
redis_client = RedisClient()

D_LINE_COORDS = [
    (41.11556, -8.60653),  # Santo Ovídio
    (41.11958, -8.60622),  # D. João II
    (41.12611, -8.60569),  # João de Deus
]

@router.post("/generate")
def generate_mock_data():
    vehicle_id = 1
    line_id = 1
    coord = random.choice(D_LINE_COORDS)
    vehicle_data = {
        "vehicle_id": vehicle_id,
        "line_id": line_id,
        "latitude": coord[0] + random.uniform(-0.0003, 0.0003),
        "longitude": coord[1] + random.uniform(-0.0003, 0.0003),
        "speed_kmh": random.uniform(30, 60),
        "timestamp": datetime.utcnow().isoformat(),
    }
    redis_client.publish_vehicle_update(vehicle_data)
    return {"message": "Vehicle data sent", "data": vehicle_data}
