import logging
from typing import Optional, Self
import asyncio
import asyncpg
from asyncpg import Connection, Pool
from fastapi import HTTPException

from shared.python.speedyapi import Logger


class Database:
    user: str
    password: str
    host: str
    port: str
    name: Optional[str] = None
    pool: Pool
    logger: Logger

    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: str,
        name: Optional[str] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.name = name
        self.logger = logger or logging.getLogger()

    def __call__(self) -> Self:
        return self

    async def initialise(self) -> None:
        self.logger.info(
            f"Connecting to db at: postgresql://{self.host}:{self.port}, "
            + f"username: {self.user if self.user is not None else 'None'}"
        )

        success = False

        while not success:
            try:
                await self._initialise()
                success = True
            except Exception as error:
                self.logger.error(f"Failed to connect to db, retyring in 5s: {error}")
                await asyncio.sleep(5)
                await self.initialise()

        self.logger.info(
            f"Connected to db at:  postgresql://{self.host}:{self.port}, "
            + f"username: {self.user if self.user is not None else 'None'}"
        )

    async def _initialise(self) -> None:
        self.pool = await asyncpg.create_pool(
            dsn=(
                "postgresql://"
                + f"{self.user}:{self.password}@"
                + f"{self.host}:{self.port}/"
                + f"{self.name or ''}"
            )
        )

    def raise_database_http_error(self, error: Exception) -> None:
        if isinstance(error, asyncpg.ForeignKeyViolationError):
            raise HTTPException(status_code=400, detail=str(error))
        raise error

    async def connection(self) -> Connection:
        async with self.pool.acquire() as connection:
            try:
                yield connection
            except Exception as error:
                Database.raise_database_http_error(error=error)

    async def transaction(self) -> Connection:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    yield connection
                except Exception as error:
                    Database.raise_database_http_error(error=error)
