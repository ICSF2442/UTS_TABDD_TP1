from bson import ObjectId

class BaseRepository:
    def __init__(self, db, collection_name: str):
        self.collection = db.get_collection(collection_name)

    def to_object_id(self, id_str: str) -> ObjectId:
        return ObjectId(id_str)

    def find_all(self):
        return list(self.collection.find())

    def find_by_id(self, id: str):
        return self.collection.find_one({"_id": self.to_object_id(id)})

    def insert(self, data: dict):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, id: str, data: dict):
        self.collection.update_one({"_id": self.to_object_id(id)}, {"$set": data})
        return self.find_by_id(id)

    def delete(self, id: str):
        self.collection.delete_one({"_id": self.to_object_id(id)})
