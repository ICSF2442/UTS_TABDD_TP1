import redis
import json

class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def publish_vehicle_update(self, vehicle_data: dict):
        self.client.xadd("vehicle_updates", {"data": json.dumps(vehicle_data)})

    def read_latest_updates(self, stream_name="vehicle_updates", count=10):
        return self.client.xrevrange(stream_name, count=count)
