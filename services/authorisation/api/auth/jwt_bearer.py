from datetime import datetime
from typing import Any, Optional
from fastapi import Depends, Query, Request, HTTPException

from shared.python.config.auth import AUTH_NAME, AUTH_SCHEME
from auth.jwt import decode_jwt
from stores.sessions import SessionsStore
from shared.python.models.authorisation import JWTAuthorizationCredentials


class AuthorisationException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        request: Request,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code,
            {
                "message": message,
                "host": request.url.hostname,
                "path": request.url.path,
                "protocol": request.url.scheme,
            },
            headers,
        )


class JWTBearer:
    async def __call__(
        self,
        request: Request,
        access_token: Optional[str] = Query(default=None),
        sessions_store: SessionsStore = Depends(SessionsStore),
    ) -> JWTAuthorizationCredentials:
        if not request.client:
            request.app.logger.error(
                "Client could not be determined on protected route."
            )
            raise AuthorisationException(
                status_code=401,
                message="Client could not be determined.",
                request=request,
            )

        auth = request.cookies.get(AUTH_NAME, None)

        if auth is None:
            auth = request.headers.get(AUTH_NAME, None)
        if auth is None and access_token:
            auth = f"{AUTH_SCHEME} {access_token}"

        if auth is None:
            request.app.logger.error(
                "Auth not sent in cookie, headers or query on protected route."
            )
            raise AuthorisationException(
                status_code=401,
                message="Invalid authorisation",
                request=request,
            )
        if auth == "":
            request.app.logger.error(
                "Empty auth in cookie, headers or query on protected route."
            )
            raise AuthorisationException(
                status_code=401,
                message="Invalid authorisation",
                request=request,
            )

        scheme, token = auth.split(" ")

        if scheme != AUTH_SCHEME:
            request.app.logger.error(
                "Invalid authentication scheme on protected route."
            )
            raise AuthorisationException(
                status_code=401,
                message="Invalid authentication scheme",
                request=request,
            )

        payload = None

        try:
            payload = decode_jwt(token=token, config=request.app.config)
        except TypeError:
            raise AuthorisationException(
                status_code=401,
                message="Invalid or expired token",
                request=request,
            )

        if payload is None:
            request.app.logger.error("Invalid config variables.")
            raise AuthorisationException(
                status_code=401,
                message="JWT decode failed",
                request=request,
            )
        if payload.get("session_id") is None:
            request.app.logger.error("No session id in token on protected route.")
            raise AuthorisationException(
                status_code=401,
                message="Invalid session",
                request=request,
            )

        session_id = payload.get("session_id")

        if session_id is None:
            request.app.logger.error("Session id not found in db on protected route.")
            raise AuthorisationException(
                status_code=401,
                message="Invalid session",
                request=request,
            )

        session = await sessions_store.get_session(id=session_id)

        if session is None:
            request.app.logger.error("Session not found in db on protected route.")
            raise AuthorisationException(
                status_code=401,
                message="Invalid session",
                request=request,
            )

        if session.ip != request.headers.get("X-Real-IP"):
            request.app.logger.error(
                f"<-- FIX ME --> Session IP ({session.ip}) does not match client "
                + f"({request.headers.get('X-Real-IP')}) on protected route."
            )
            # raise AuthorisationException(
            #     status_code=401,
            #     message="Invalid session",
            #     request=request,
            # )
        if session.expires <= datetime.utcnow():
            request.app.logger.error(
                f"Session expired ({session.expires.isoformat()}) on protected route."
            )
            raise AuthorisationException(
                status_code=401,
                message="Session expired",
                request=request,
            )
        if session.disabled:
            request.app.logger.error("Session disabled on protected route.")
            raise AuthorisationException(
                status_code=401,
                message="Session expired",
                request=request,
            )

        return JWTAuthorizationCredentials(
            scheme=scheme,
            token=token,
            session=session,
        )
