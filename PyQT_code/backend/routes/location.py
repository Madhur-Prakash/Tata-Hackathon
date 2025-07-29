from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Handle both relative and absolute imports
try:
    from ..models import LocationIn, RouteHistory
    from ..database import SessionLocal
    from ..services.charging_service import get_nearest_station
except ImportError:
    from models import LocationIn, RouteHistory
    from database import SessionLocal
    from services.charging_service import get_nearest_station

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/update")
def update_location(data: LocationIn, db: Session = Depends(get_db)):
    entry = RouteHistory(lat=data.lat, lng=data.lng, battery=data.batteryLevel)
    db.add(entry)
    db.commit()

    if data.batteryLevel < 25:
        station = get_nearest_station(data.lat, data.lng)
        return {"redirectToChargingStation": True, "station": station}
    
    return {"redirectToChargingStation": False}
