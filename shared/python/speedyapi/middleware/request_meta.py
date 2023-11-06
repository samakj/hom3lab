from datetime import datetime
from uuid import uuid4

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class RequestMetaMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = datetime.utcnow()

        request_id = uuid4().hex

        response = await call_next(request)

        end_time = datetime.utcnow()
        duration = end_time - start_time

        response.headers["X-Request-Id"] = request_id
        response.headers["X-Request-Start"] = str(
            round(start_time.timestamp() * 1000, ndigits=3)
        )
        response.headers["X-Request-End"] = str(
            round(end_time.timestamp() * 1000, ndigits=3)
        )
        response.headers["X-Request-Duration"] = str(
            round(duration.total_seconds() * 1000, ndigits=3)
        )

        return response
