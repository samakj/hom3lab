from datetime import datetime
from typing import Optional
from pydantic import BaseModel, IPvAnyAddress, Field


class CreateDevice(BaseModel):
    mac: str = Field(description="The mac address of the device.")
    location_id: int = Field(
        description="The id of the location where the device is located."
    )


class Device(CreateDevice):
    id: int = Field(description="The id of the device.")
