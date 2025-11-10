from fastapi import APIRouter
import time, random
from services.utils.tracking_client import TrackingClient

router = APIRouter(prefix="/mock", tags=["Mock Tracking"])

GAIA_LINE = [
    (41.11556, -8.60653),  # Santo Ovídio
    (41.11958, -8.60622),  # D. João II
    (41.12611, -8.60569)   # João de Deus
]

@router.post("/simulate")
def simulate_vehicle(line_id: int = 1, vehicle_id: int = 101):

    for i, (lat, lon) in enumerate(GAIA_LINE):
        speed = random.uniform(25, 40)
        print(f" Sending position {i+1}: ({lat}, {lon})")

        result = TrackingClient.send_position(
            vehicle_id=vehicle_id,
            line_id=line_id,
            latitude=lat,
            longitude=lon,
            speed_kmh=speed
        )

        time.sleep(5)

    return {"status": "simulation_complete"}
