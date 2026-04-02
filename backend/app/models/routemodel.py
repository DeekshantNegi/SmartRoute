from pydantic import BaseModel

class RouteRequest(BaseModel):
    source: str
    destination: str