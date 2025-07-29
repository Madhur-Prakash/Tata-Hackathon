from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

# For relative imports when running as module
try:
    from .database import Base
except ImportError:
    # For direct execution
    from database import Base

class LocationIn(BaseModel):
    lat: float
    lng: float
    batteryLevel: int

class RouteRequest(BaseModel):
    start: list[float]
    end: list[float]

class RouteHistory(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    battery = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
