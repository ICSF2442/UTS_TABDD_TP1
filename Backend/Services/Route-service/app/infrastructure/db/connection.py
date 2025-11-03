from pymongo import MongoClient
from app.core.config import settings


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]

    def get_collection(self, name: str):
        return self.db[name]


# settings.MONGO_URI = "mongodb://localhost:27017"
# settings.MONGO_DB_NAME = "urban_transport"
