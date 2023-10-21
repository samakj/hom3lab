import inspect
import json
import logging
from functools import wraps
from typing import Any, Callable, Optional, Self
from fastapi import Request, Response
from pydantic import BaseModel
from aioredis import Redis
from shared.python.models.authorisation import UserCredentials

from shared.python.extensions.speedyapi import Logger
from shared.python.json import serialise_json, parse_json


class Cache:
    host: str
    port: str
    logger: Logger
    user: Optional[str]
    password: Optional[str]
    name: Optional[str]
    client: Optional[Redis]
    alias: Optional[dict[str, str]]

    def __init__(
        self,
        host: str,
        port: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        logger: Optional[Logger] = None,
        alias: Optional[dict[str, str]] = None,
    ) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.name = name
        self.client = None
        self.logger = logger or logging.getLogger()
        self.alias = alias

    def __call__(self) -> Self:
        return self

    async def initialise(self) -> None:
        self.logger.info(
            f"Connecting to cache at: redis://{self.host}:{self.port}, "
            + f"username: {self.user if self.user is not None else 'None'}"
        )

        user_prefix = ""
        cache_name_suffix = ""

        if self.user is not None:
            user_prefix = f"{self.user}"
            if self.password is not None:
                user_prefix += f":{self.password}"
            user_prefix += "@"
        if self.name is not None:
            cache_name_suffix = f"/{self.name}"

        try:
            self.client = await Redis.from_url(
                f"redis://{user_prefix}{self.host}:{self.port}{cache_name_suffix}"
            )

            self.logger.info(
                f"Connected to cache at:  redis://{self.host}:{self.port}, "
                + f"username: {self.user if self.user is not None else 'None'}"
            )
        except Exception as error:
            self.logger.error(f"Failed to connect to cache: {error}")

    def alias_key(self, key: str) -> str:
        if self.alias is not None:
            for value, alias in self.alias.items():
                key = str(key).replace(value, alias)

        return key

    async def get[T](self, key: str) -> T:
        key = self.alias_key(key=key)
        value = None

        if self.client is not None:
            try:
                cache_value = await self.client.get(key)

                if cache_value is not None:
                    value = parse_json(cache_value)
            except Exception as error:
                self.logger.error(f"Errored when getting '{key}' from cache: {error}")
        else:
            self.logger.warn("Cache not connected.")

        if value is None:
            value = await self.set(key=key)

        return value

    async def set[T](
        self, key: str, value: Optional[Any] = None, expiry: Optional[int] = None
    ) -> T:
        key = self.alias_key(key=key)
        if self.client is not None:
            if value is not None:
                try:
                    await self.client.set(key, serialise_json(value), ex=expiry)
                except Exception as error:
                    self.logger.error(f"Errored when setting '{key}' in cache: {error}")
            else:
                await self.clear(key=key)

        return value

    async def clear(self, key: str) -> None:
        key = self.alias_key(key=key)
        if self.client is not None:
            try:
                await self.client.delete(key)
            except Exception as error:
                self.logger.error(f"Errored when setting '{key}' in cache: {error}")

    async def clear_pattern(
        self, pattern: str, condition: Optional[Callable[[Any], bool]] = None
    ) -> None:
        key = self.alias_key(key=pattern)
        if self.client is not None:
            for key in await self.client.keys(pattern):
                clear = (
                    condition(await self.get(key=key))
                    if condition is not None
                    else True
                )
                if clear:
                    await self.clear(key=key)

    def create_route_key(
        self,
        request: Request,
        credentials: Optional[UserCredentials] = None,
        include_query_params: bool = True,
        include_access_token: bool = False,
    ) -> str:
        key = ""
        key += request.url.hostname or ""
        key += f":{request.url.port}" if request.url.port else ""
        key += request.url.path

        if key.endswith("/"):
            key = key[:-1]

        search: list[str] = []

        if include_access_token and credentials is not None:
            search.append(f"access_token={credentials.token}")

        if include_query_params:
            for param, value in request.query_params.items():
                if param != "access_token":
                    search.append(f"{param}={value}")

        if search:
            search.sort()
            key += "?"
            key += "&".join(search)

        return self.alias_key(key=key)

    def route(self, expiry: int = 60, include_access_token: bool = False) -> Any:
        def decorator(func):
            signature = inspect.signature(func)
            has_request_param = False
            has_response_param = False

            for param in signature.parameters.values():
                if param.annotation is Request:
                    has_request_param = True
                if param.annotation is Response:
                    has_response_param = True

            parameters = [*signature.parameters.values()]
            if not has_request_param:
                parameters.append(
                    inspect.Parameter(
                        name="request",
                        annotation=Request,
                        kind=inspect.Parameter.KEYWORD_ONLY,
                    ),
                )
            if not has_response_param:
                parameters.append(
                    inspect.Parameter(
                        name="response",
                        annotation=Response,
                        kind=inspect.Parameter.KEYWORD_ONLY,
                    ),
                )
            if parameters:
                signature = signature.replace(parameters=parameters)
            func.__signature__ = signature

            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = (
                    kwargs.get("request")
                    if has_request_param
                    else kwargs.pop("request")
                )
                response = (
                    kwargs.get("response")
                    if has_request_param
                    else kwargs.pop("response")
                )
                user_credentials = kwargs.get(
                    "user_credentials", kwargs.get("permissions")
                )
                if not request:
                    self.logger.info("no-store request not cached")
                    return await func(*args, **kwargs)
                if request.headers.get("Cache-Control") == "no-store":
                    self.logger.info("no-store request not cached")
                    return await func(*args, **kwargs)
                if request.method != "GET":
                    self.logger.info("Non-get request not cached")
                    return await func(*args, **kwargs)

                response.headers["X-Will-Cache"] = "true"
                response.headers["X-Cache-Duration"] = f"{expiry}"
                key = self.create_route_key(
                    request=request,
                    credentials=user_credentials,
                    include_query_params=True,
                    include_access_token=include_access_token,
                )
                cached_value = await self.get(key=key)

                if cached_value:
                    response.headers["X-Cached-Value"] = "true"
                    return cached_value

                value = await func(*args, **kwargs)

                if isinstance(value, BaseModel):
                    value = dict(value)

                return await self.set(key=key, value=value, expiry=expiry)

            return wrapper

        return decorator
