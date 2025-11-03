import time
from pymongo import MongoClient
import redis
import json
from datetime import datetime

class TripSyncWorker:
    def __init__(self, redis_host="localhost", redis_port=6379, mongo_uri="mongodb://localhost:27017", mongo_db="urban_transport"):
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.mongo = MongoClient(mongo_uri)[mongo_db]
        self.trips = self.mongo["trips"]

    def start(self):
        print("🚦 TripSyncWorker started. Listening for Redis trip updates...")
        last_id = "0-0"
        while True:
            events = self.redis.xread({"trip_updates": last_id}, block=5000, count=10)
            if not events:
                continue
            for stream, messages in events:
                for msg_id, data in messages:
                    last_id = msg_id
                    self.process_event(data)

    def process_event(self, data):
        try:
            trip_id = data["trip_id"]
            delay_minutes = int(data.get("delay_minutes", 0))
            status = data.get("status", "in_progress")

            print(f"🔄 Updating trip {trip_id} → delay: {delay_minutes}, status: {status}")

            result = self.trips.update_one(
                {"_id": trip_id},
                {"$set": {
                    "delay_minutes": delay_minutes,
                    "status": status,
                    "updated_at": datetime.utcnow().isoformat()
                }}
            )

            if result.matched_count == 0:
                print(f" Trip {trip_id} not found in MongoDB")
        except Exception as e:
            print(f"Error processing event: {e}")
