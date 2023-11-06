from fastapi import APIRouter
from pydantic import BaseModel

PING_ROUTER = APIRouter()


class PingResponse(BaseModel):
    ping: str = "pong"


@PING_ROUTER.get("/v0/ping", response_model=PingResponse, tags=["default"])
def ping() -> PingResponse:
    return PingResponse()
