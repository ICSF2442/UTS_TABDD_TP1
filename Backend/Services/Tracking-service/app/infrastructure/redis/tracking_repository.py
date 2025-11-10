from datetime import datetime
import json
from app.infrastructure.redis.connection import RedisConnection


class TrackingRepository:
    def __init__(self):
        self.redis = RedisConnection().get_client()
        self.stream_name = "vehicle_updates"

    # Store latest position
    def update_vehicle_position(self, position):
        key = f"vehicle:{position.vehicle_id}"
        data = {
            "line_id": position.line_id,
            "latitude": position.latitude,
            "longitude": position.longitude,
            "speed": position.speed,
            "timestamp": position.timestamp.isoformat(),
        }
        self.redis.hset(key, mapping=data)
        self.redis.zadd(f"{key}:positions", {json.dumps(data): datetime.now().timestamp()})

        # Broadcast via stream
        self.redis.xadd("tracking_updates", data)

    # Get latest position
    def get_latest_position(self, vehicle_id: int):
        key = f"vehicle:{vehicle_id}"
        return self.redis.hgetall(key)

    # Get last N positions (for route replay)
    def get_last_positions(self, vehicle_id: int, count: int = 10):
        key = f"vehicle:{vehicle_id}:positions"
        results = self.redis.zrevrange(key, 0, count - 1)
        return [json.loads(r) for r in results]

    # Store delay info
    def update_delay(self, trip_id: int, delay_minutes: int):
        key = f"trip:{trip_id}:status"
        self.redis.hset(key, mapping={"delay_minutes": delay_minutes, "updated_at": datetime.now().isoformat()})

    def publish_trip_update(self, trip_id: int, delay_minutes: int, status: str = "delayed"):
        event = {
            "trip_id": trip_id,
            "delay_minutes": delay_minutes,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        self.redis.xadd("trip_updates", event)

    def publish_notification(self, line_id: int, delay_minutes: int):
        message = {
            "event": "line_delay",
            "line_id": line_id,
            "delay_minutes": delay_minutes,
        }
        self.redis.publish("notifications", json.dumps(message))


