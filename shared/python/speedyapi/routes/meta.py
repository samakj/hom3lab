from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

META_ROUTER = APIRouter()


class MetaResponse(BaseModel):
    timestamp: datetime


@META_ROUTER.get("/v0/meta", response_model=MetaResponse, tags=["default"])
def meta() -> MetaResponse:
    return MetaResponse(timestamp=datetime.now())
