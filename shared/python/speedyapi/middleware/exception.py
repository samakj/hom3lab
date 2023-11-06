from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
        except HTTPException as error:
            return JSONResponse(
                content={"status_code": error.status_code, "detail": error.detail},
                status_code=error.status_code,
            )
        except Exception as error:
            if await request.is_disconnected():
                return JSONResponse(status_code=400, content="Client disconnect")

            request.app.logger.exception(error)
            return JSONResponse(
                content={"status_code": 500, "detail": str(error)},
                status_code=500,
            )
        return response
