from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateSession(BaseModel):
    user_id: int = Field(description="The id of the user the session is for.")
    ip: Optional[str] = Field(
        description="The ip attatched to the session.", default=None
    )


class Session(BaseModel):
    id: int = Field(description="The session id.")
    user_id: int = Field(description="The id of the user the session is for.")
    created: datetime = Field(description="The creation date of the session.")
    expires: datetime = Field(description="The expiry date of the session.")
    ip: Optional[str] = Field(
        description="The ip attatched to the session.", default=None
    )
    disabled: bool = Field(
        description="Whether the session has been manually disabled or not.",
        default=False,
    )
