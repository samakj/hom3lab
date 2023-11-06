from typing import Optional
from fastapi import HTTPException, Query, Depends, Request

from cache import cache
from auth.bearer_permission import BearerPermission, PermissionCredentials
from stores.sessions import SessionsStore, sessions_store
from shared.python.speedyapi import APIRouter
from shared.python.cache import Cache
from shared.python.models.session import Session, CreateSession


SESSIONS_V0_ROUTER = APIRouter(prefix="/v0/sessions", tags=["sessions"])


@SESSIONS_V0_ROUTER.get("/{id:int}", response_model=Session)
@cache.route(expiry=60)
async def get_session(
    id: int,
    sessions_store: SessionsStore = Depends(sessions_store),
    permissions: PermissionCredentials = Depends(
        BearerPermission(scope="sessions.get")
    ),
) -> Session:
    session = await sessions_store.get_session(id=id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    return session


@SESSIONS_V0_ROUTER.get("/", response_model=list[Session])
@cache.route(expiry=60)
async def get_sessions(
    id: Optional[list[int]] = Query(default=None),
    user_id: Optional[list[int]] = Query(default=None),
    ip: Optional[list[str]] = Query(default=None),
    sessions_store: SessionsStore = Depends(sessions_store),
    permissions: PermissionCredentials = Depends(
        BearerPermission(scope="sessions.get")
    ),
) -> Session:
    session = await sessions_store.get_sessions(id=id, user_id=user_id, ip=ip)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    return session


@SESSIONS_V0_ROUTER.post("/", response_model=Session)
async def create_session(
    session: CreateSession,
    request: Request,
    sessions_store: SessionsStore = Depends(sessions_store),
    cache: Cache = Depends(cache),
    permissions: PermissionCredentials = Depends(
        BearerPermission(scope="sessions.create")
    ),
) -> Session:
    session = await sessions_store.create_session(session=session)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    await cache.clear_pattern(
        pattern=cache.create_route_key(request=request, include_query_params=False)
        + "*"
    )

    return session


@SESSIONS_V0_ROUTER.patch("/{id:int}", response_model=Session)
async def update_session(
    id: int,
    session: Session,
    request: Request,
    sessions_store: SessionsStore = Depends(sessions_store),
    cache: Cache = Depends(cache),
    permissions: PermissionCredentials = Depends(
        BearerPermission(scope="sessions.update")
    ),
) -> Session:
    session = await sessions_store.update_session(session=session)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    await cache.clear_pattern(
        pattern=cache.create_route_key(request=request, include_query_params=False)
        + "*"
    )

    return session


@SESSIONS_V0_ROUTER.delete("/{id:int}")
async def delete_session(
    id: int,
    request: Request,
    sessions_store: SessionsStore = Depends(sessions_store),
    cache: Cache = Depends(cache),
    permissions: PermissionCredentials = Depends(
        BearerPermission(scope="sessions.delete")
    ),
) -> None:
    await sessions_store.delete_session(id=id)

    await cache.clear_pattern(
        pattern=cache.create_route_key(request=request, include_query_params=False)
        + "*"
    )

    return None
