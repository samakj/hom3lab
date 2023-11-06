from fastapi import HTTPException

from shared.python.speedyapi import APIRouter
from shared.python.models.location import CreateLocation, Location
from shared.python.helpers.load_json_file import load_json_file

LOCATIONS_V0_ROUTER = APIRouter(prefix="/v0/locations", tags=["locations"])

@LOCATIONS_V0_ROUTER.get("/{id:int}", response_model=Location)
def get_location(id: int) -> Location:
    for location in load_json_file("test-data/locations.json"):
        if location["id"] == id:
            return Location.parse_obj(location)
    
    raise HTTPException(status=404)

@LOCATIONS_V0_ROUTER.get("/", response_model=list[Location])
def get_locations() -> Location:
    return [
        Location.parse_obj(location)
        for location in load_json_file("test-data/locations.json")
    ]

@LOCATIONS_V0_ROUTER.post("/", response_model=Location)
def create_location(location: CreateLocation) -> Location:
    return Location.parse_obj(load_json_file("test-data/locations.json")[0])

@LOCATIONS_V0_ROUTER.patch("/{id:int}", response_model=Location)
def create_location(id:int, location: CreateLocation) -> Location:
    return get_location(id)
