from typing import Optional
from pydantic import BaseModel, Field


class CreateLocation(BaseModel):
    name: str = Field(description="The name of the location.")
    tags: Optional[list[str]] = Field(description="A list of tags for the location.")


class Location(CreateLocation):
    id: int = Field(description="The id of the location.")
