from app.domain.models.base_model import MongoBaseModel

class LineStop(MongoBaseModel):
    line_id: str
    stop_id: str
    stop_order: int
