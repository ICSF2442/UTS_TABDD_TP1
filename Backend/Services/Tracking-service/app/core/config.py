import os


class Settings:
    REDIS_HOST = "redis-14107.crce202.eu-west-3-1.ec2.redns.redis-cloud.com"
    REDIS_PORT = 14107
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    REDIS_STREAM_UPDATES = "tracking_updates"

settings = Settings()
