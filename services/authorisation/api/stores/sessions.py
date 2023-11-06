from datetime import datetime
from typing import Optional, Union, Self

from database import database

from shared.python.models.session import Session, CreateSession
from stores.queries.sessions import (
    GET_SESSION_BY_ID,
    GET_SESSIONS,
    CREATE_SESSION,
    UPDATE_SESSION,
    DELETE_SESSION,
)
from shared.python.helpers.to_filter import to_filter, to_array_filter


class SessionsStore:
    def __call__(self) -> Self:
        return self

    async def get_session(self, id: int) -> Optional[Session]:
        connection = await database.transaction()
        response = await connection.fetchrow(GET_SESSION_BY_ID.format(id=to_filter(id)))
        return Session(**dict(response)) if response is not None else None

    async def get_sessions(
        self,
        id: Optional[Union[int, list[int]]] = None,
        user_id: Optional[Union[int, list[int]]] = None,
        ip: Optional[Union[str, list[str]]] = None,
        disabled: Optional[bool] = None,
        created_gte: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        expires_gte: Optional[datetime] = None,
        expires_lte: Optional[datetime] = None,
    ) -> list[Session]:
        where = []

        if id is not None:
            where.append(f"id IN {to_array_filter(id)}")
        if user_id is not None:
            where.append(f"user_id IN {to_array_filter(user_id)}")
        if ip is not None:
            where.append(f"ip IN {to_array_filter(ip)}")
        if disabled is not None:
            where.append(f"disabled = {to_filter(disabled)}")
        if created_gte is not None:
            where.append(f"created >= {to_filter(created_gte)}")
        if created_lte is not None:
            where.append(f"created <= {to_filter(created_lte)}")
        if expires_gte is not None:
            where.append(f"expires >= {to_filter(expires_gte)}")
        if expires_lte is not None:
            where.append(f"expires <= {to_filter(expires_lte)}")

        connection = await database.transaction()
        response = await connection.fetch(
            GET_SESSIONS.format(where=" AND ".join(where) if where else "TRUE")
        )

        return [Session(**dict(row)) for row in response]

    async def create_session(
        self,
        session: CreateSession,
    ) -> Optional[Session]:
        connection = await database.transaction()
        row = await connection.fetchrow(
            CREATE_SESSION.format(
                user_id=to_filter(session.user_id),
                created=to_filter(datetime.utcnow()),
                expires=to_filter(datetime.utcnow() + SESSION_DURATION),
                ip=to_filter(session.ip),
                disabled=to_filter(False),
            )
        )
        return await self.get_session(id=row["id"])

    async def update_session(self, session: Session) -> Optional[Session]:
        connection = await database.transaction()
        await connection.execute(
            UPDATE_SESSION.format(
                id=to_filter(session.id),
                user_id=to_filter(session.user_id),
                created=to_filter(session.created),
                expires=to_filter(session.expires),
                ip=to_filter(session.ip),
                disabled=to_filter(session.disabled),
            )
        )
        return await self.get_session(id=session.id)

    async def delete_session(self, id: int) -> None:
        connection = await database.transaction()
        await connection.execute(DELETE_SESSION.format(id=to_filter(id)))


sessions_store = SessionsStore()
