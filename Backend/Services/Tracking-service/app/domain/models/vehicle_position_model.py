from datetime import datetime
from pydantic import BaseModel


class VehiclePosition(BaseModel):
    vehicle_id: str
    line_id: str
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime
