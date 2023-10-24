import click
import os

from config import root_folder
from services.postgres import postgres, build as build_postgres
from services.redis import redis, build as build_redis


@click.group()
def services() -> None:
    pass


@services.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    build_postgres.invoke(ctx=ctx)
    build_redis.invoke(ctx=ctx)


@services.command()
@click.pass_context
def run(ctx: click.Context) -> None:
    build_postgres.invoke(ctx=ctx)
    build_redis.invoke(ctx=ctx)
    os.system(
        f"""
docker-compose \
    -f {root_folder}/services/postgres/docker-compose.yml \
    -f {root_folder}/services/redis/docker-compose.yml \
    up
"""
    )


services.add_command(cmd=postgres)
services.add_command(cmd=redis)
