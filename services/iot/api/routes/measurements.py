from fastapi import HTTPException

from shared.python.speedyapi import APIRouter
from shared.python.models.measurement import CreateMeasurement, Measurement
from shared.python.helpers.load_json_file import load_json_file

MEASUREMENTS_V0_ROUTER = APIRouter(prefix="/v0/measurements", tags=["measurements"])

@MEASUREMENTS_V0_ROUTER.get("/{id:int}", response_model=Measurement)
def get_measurement(id: int) -> Measurement:
    for measurement in load_json_file("test-data/measurements.json"):
        if measurement["id"] == id:
            return Measurement.parse_obj(measurement)
    
    raise HTTPException(status=404)

@MEASUREMENTS_V0_ROUTER.get("/", response_model=list[Measurement])
def get_measurements() -> Measurement:
    return [
        Measurement.parse_obj(measurement)
        for measurement in load_json_file("test-data/measurements.json")
    ]

@MEASUREMENTS_V0_ROUTER.post("/", response_model=Measurement)
def create_measurement(measurement: CreateMeasurement) -> Measurement:
    return Measurement.parse_obj(load_json_file("test-data/measurements.json")[0])

@MEASUREMENTS_V0_ROUTER.patch("/{id:int}", response_model=Measurement)
def create_measurement(id:int, measurement: CreateMeasurement) -> Measurement:
    return get_measurement(id)
