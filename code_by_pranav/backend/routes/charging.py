from fastapi import APIRouter
from fastapi import Query

# Handle both relative and absolute imports
try:
    from ..services.charging_service import get_nearest_station
except ImportError:
    from services.charging_service import get_nearest_station

router = APIRouter()

@router.get("/")
def fetch_charger(lat: float = Query(...), lng: float = Query(...)):
    return get_nearest_station(lat, lng)
