import redis
import json
from datetime import datetime
from app.infrastructure.db.connection import SessionLocal
from app.infrastructure.db.notification_repository import NotificationRepository
from app.infrastructure.db.user_repository import UserRepository
from app.infrastructure.redis.connection import RedisConnection


class NotificationConsumer:
    def __init__(self, redis_host="localhost", redis_port=6379):
        self.redis = RedisConnection().get_client()
        self.db = SessionLocal()
        self.user_repo = UserRepository(self.db)
        self.notification_repo = NotificationRepository(self.db)

    def start(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe("notifications")
        print("Listening for notifications on Redis channel 'notifications'...")

        for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                self.handle_event(data)

    def handle_event(self, data):
        if data["event"] == "line_delay":
            line_id = data["line_id"]
            delay = data["delay_minutes"]

            print(f" Received delay notification for line {line_id} ({delay} min)")

            # Find all users who have this line as a favorite
            users = self.user_repo.find_users_with_favorite(line_id)

            for user in users:
                self.notification_repo.save_notification(
                    user_id=user.user_id,
                    line_id=line_id,
                    message=f"Line {line_id} is delayed by {delay} minutes.",
                    type="delay"
                )
