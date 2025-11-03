import redis
from app.core.config import settings


class RedisConnection:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    def get_client(self):
        return self.client


# REDIS_HOST = "localhost"
# REDIS_PORT = 6379
