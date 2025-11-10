import redis
import os
from app.core.config import settings


class RedisConnection:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host="",
            port=14107,
            password="",  # store in .env
            decode_responses=True
        )

    def get_client(self):
        return self.redis_client
