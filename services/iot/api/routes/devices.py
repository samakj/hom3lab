from fastapi import HTTPException

from shared.python.speedyapi import APIRouter
from shared.python.models.device import CreateDevice, Device
from shared.python.helpers.load_json_file import load_json_file

DEVICES_V0_ROUTER = APIRouter(prefix="/v0/devices", tags=["devices"])

@DEVICES_V0_ROUTER.get("/{id:int}", response_model=Device)
def get_device(id: int) -> Device:
    for device in load_json_file("test-data/devices.json"):
        if device["id"] == id:
            return Device.parse_obj(device)
    
    raise HTTPException(status=404)

@DEVICES_V0_ROUTER.get("/", response_model=list[Device])
def get_devices() -> Device:
    return [
        Device.parse_obj(device)
        for device in load_json_file("test-data/devices.json")
    ]

@DEVICES_V0_ROUTER.post("/", response_model=Device)
def create_device(device: CreateDevice) -> Device:
    return Device.parse_obj(load_json_file("test-data/devices.json")[0])

@DEVICES_V0_ROUTER.patch("/{id:int}", response_model=Device)
def create_device(id:int, device: CreateDevice) -> Device:
    return get_device(id)
