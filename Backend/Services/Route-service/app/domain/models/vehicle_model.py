from app.domain.models.base_model import MongoBaseModel

class Vehicle(MongoBaseModel):
    vehicle_id: str
    line_id: str
    plate_number: str
    capacity: int
    status: str
    type: str
