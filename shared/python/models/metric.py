from typing import Optional
from pydantic import BaseModel, Field


class CreateMetric(BaseModel):
    name: str = Field(description="The name of the metric.")
    abbreviation: str = Field(description="The abbreviation of the metric.")
    unit: Optional[str] = Field(description="The unit of the metric.", default=None)


class Metric(BaseModel):
    id: int = Field(description="The id of the metric.")
