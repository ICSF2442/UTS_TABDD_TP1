from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class RouteStopBase(BaseModel):
    name: str
    type: str
    stop_id: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class RouteSegmentBase(BaseModel):
    from_stop: str
    to_stop: str
    transport: str
    line: str
    time_min: int
    distance_km: float

class RouteRequest(BaseModel):
    origin: str
    destination: str
    
    @validator('origin', 'destination')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Origem/destino não pode estar vazio')
        return v.strip()

class RouteResponse(BaseModel):
    total_time_minutes: float
    stops: List[RouteStopBase]
    segments: List[RouteSegmentBase]
    transfer_count: int
    message: str
    
    class Config:
        from_attributes = True