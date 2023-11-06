from datetime import datetime
from decimal import Decimal
from typing import Optional, Union
from pydantic import BaseModel, Field


class CreateMeasurement(BaseModel):
    timestamp: datetime = Field(
        description="The timestamp when the metric was reported."
    )
    device_id: int = Field(description="The device id of the measurement.")
    location_id: int = Field(description="The location id of the measurement.")
    metric_id: int = Field(description="The metric id of the measurement.")
    tags: Optional[list[str]] = Field(description="A list of tags for the measurement.")
    value:  Union[bool, Decimal, int, str, None] = Field(description="The value measured.", default=None)


class Measurement(CreateMeasurement):
    id: int = Field(description="The id of the measurement.")
