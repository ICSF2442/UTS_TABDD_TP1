from datetime import datetime
from typing import List, Dict, Any

class RouteStop:
    def __init__(self, name: str, type: str, stop_id: str, latitude: float = None, longitude: float = None):
        self.name = name
        self.type = type
        self.stop_id = stop_id
        self.latitude = latitude
        self.longitude = longitude

class RouteSegment:
    def __init__(self, from_stop: str, to_stop: str, transport: str, line: str, time_min: int, distance_km: float):
        self.from_stop = from_stop
        self.to_stop = to_stop
        self.transport = transport
        self.line = line
        self.time_min = time_min
        self.distance_km = distance_km

class OptimalRoute:
    def __init__(self, total_time_minutes: float, stops: List[RouteStop], segments: List[RouteSegment], transfer_count: int = 0):
        self.total_time_minutes = total_time_minutes
        self.stops = stops
        self.segments = segments
        self.transfer_count = transfer_count
        self.created_at = datetime.now()