from pydantic import BaseModel


class LocationIn(BaseModel):
    lat: float
    lng: float
    batteryLevel: int

class RouteRequest(BaseModel):
    start: list[float]
    end: list[float]

