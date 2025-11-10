import requests
from datetime import datetime
from core.config import settings

class TrackingClient:
    @staticmethod
    def send_position(vehicle_id: int, line_id: int, latitude: float, longitude: float, speed_kmh: float):
        data = {
            "vehicle_id": vehicle_id,
            "line_id": line_id,
            "latitude": latitude,
            "longitude": longitude,
            "speed_kmh": speed_kmh,
            "timestamp": datetime.now().isoformat()
        }
        response = requests.post(settings.TRACKING_SERVICE_URL, json=data, timeout=5)
        response.raise_for_status()
        return response.json()
