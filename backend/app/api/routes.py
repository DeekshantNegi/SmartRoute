from fastapi import APIRouter
from app.models.routemodel import RouteRequest
from app.services.route_service import find_routes

router = APIRouter()

@router.post("/route")
def get_route(data: RouteRequest):

    routes = find_routes(data.source, data.destination)

    return routes