from app.domain.models.base_model import MongoBaseModel

class Line(MongoBaseModel):
    line_name: str
    origin: str
    destination: str
    operating_hours: str
    type: str
