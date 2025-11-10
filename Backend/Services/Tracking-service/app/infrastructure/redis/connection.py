import redis
import os
from app.core.config import settings


class RedisConnection:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host="redis-14107.crce202.eu-west-3-1.ec2.redns.redis-cloud.com",
            port=14107,
            password="9ReTNLIrZptjx2dE9hCG1163zOsS80yw",  # store in .env
            decode_responses=True
        )

    def get_client(self):
        return self.redis_client
