from fastapi import APIRouter

# Handle both relative and absolute imports
try:
    from ..models import RouteRequest
    from ..services.routing_service import get_route
except ImportError:
    from models import RouteRequest
    from services.routing_service import get_route

router = APIRouter()

@router.post("/")
def fetch_route(data: RouteRequest):
    return get_route(data.start, data.end)
