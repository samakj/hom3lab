from typing import Optional, Union, Self

from fastapi import Request
from passlib.context import CryptContext

from database import database

from shared.python.models.user import User, CreateUser
from stores.queries.users import (
    GET_USER_BY_ID,
    GET_USER_BY_USERNAME,
    GET_USERS,
    CREATE_USER,
    UPDATE_USER,
    UPDATE_USER_PASSWORD,
    DELETE_USER,
)
from shared.python.helpers.to_filter import to_filter, to_array_filter


class UsersStore:
    password_context: CryptContext

    def __call__(self, request: Request) -> Self:
        self.password_context = request.app.password_context
        return self

    async def get_user(self, id: int) -> Optional[User]:
        connection = await database.transaction()
        response = await connection.fetchrow(GET_USER_BY_ID.format(id=to_filter(id)))
        return User(**dict(response)) if response is not None else None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        connection = await database.transaction()
        response = await connection.fetchrow(
            GET_USER_BY_USERNAME.format(username=to_filter(username))
        )
        return User(**dict(response)) if response is not None else None

    async def get_users(
        self,
        id: Optional[Union[int, list[int]]] = None,
        username: Optional[Union[str, list[str]]] = None,
        name: Optional[Union[str, list[str]]] = None,
        scopes: Optional[Union[str, list[str]]] = None,
    ) -> list[User]:
        where = []

        if id is not None:
            where.append(f"id IN {to_array_filter(id)}")
        if username is not None:
            where.append(f"username IN {to_array_filter(username)}")
        if name is not None:
            where.append(f"name IN {to_array_filter(name)}")
        if scopes is not None:
            where.append(f"scopes @> {to_array_filter(name)}")

        connection = await database.transaction()
        response = await connection.fetch(
            GET_USERS.format(where=" AND ".join(where) if where else "TRUE")
        )

        return [User(**dict(row)) for row in response]

    async def create_user(self, user: CreateUser) -> Optional[User]:
        connection = await database.transaction()
        row = await connection.fetchrow(
            CREATE_USER.format(
                username=to_filter(user.username),
                password=to_filter(self.password_context.hash(user.password)),
                name=to_filter(user.name),
                scopes=to_array_filter(user.scopes),
            )
        )
        return await self.get_user(id=row["id"])

    async def update_user(self, user: User) -> Optional[User]:
        connection = await database.transaction()
        await connection.execute(
            UPDATE_USER.format(
                id=to_filter(user.id),
                username=to_filter(user.username),
                name=to_filter(user.name),
                scopes=to_array_filter(user.scopes),
            )
        )
        return await self.get_user(id=user.id)

    async def update_user_password(self, user: User) -> Optional[User]:
        connection = await database.transaction()
        await connection.execute(
            UPDATE_USER_PASSWORD.format(
                id=to_filter(user.id),
                username=to_filter(user.username),
                password=to_filter(self.password_context.hash(user.password)),
                name=to_filter(user.name),
                scopes=to_array_filter(user.scopes),
            )
        )
        return await self.get_user(id=user.id)

    async def delete_user(self, id: int) -> None:
        connection = await database.transaction()
        await connection.execute(DELETE_USER.format(id=to_filter(id)))

    async def verify_user_password(
        self, username: str, password: str
    ) -> Optional[User]:
        user = await self.get_user_by_username(username=username)

        if user is None:
            return None

        success = False

        try:
            success = self.password_context.verify(secret=password, hash=user.password)
        except Exception:
            pass

        return user if success else None


users_store = UsersStore()
