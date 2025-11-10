from datetime import datetime

class VehiclePosition:
    def __init__(self, vehicle_id: int, line_id: int, latitude: float, longitude: float, speed: float, timestamp: datetime):
        self.vehicle_id = vehicle_id
        self.line_id = line_id
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "line_id": self.line_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "speed_kmh": self.speed,
            "timestamp": self.timestamp.isoformat(),
        }
