import click
import os

from config import root_folder
from services.authorisation import authorisation, build as build_authorisation
from services.iot import iot, build as build_iot
from services.postgres import postgres, build as build_postgres
from services.redis import redis, build as build_redis


@click.group()
def services() -> None:
    pass


@services.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    build_authorisation.invoke(ctx=ctx)
    build_iot.invoke(ctx=ctx)
    build_postgres.invoke(ctx=ctx)
    build_redis.invoke(ctx=ctx)


@services.command()
@click.pass_context
def run(ctx: click.Context) -> None:
    build_authorisation.invoke(ctx=ctx)
    build_iot.invoke(ctx=ctx)
    build_postgres.invoke(ctx=ctx)
    build_redis.invoke(ctx=ctx)
    os.system(
        f"""
docker-compose \
    -f {root_folder}/services/authorisation/api/docker-compose.yml \
    -f {root_folder}/services/iot/api/docker-compose.yml \
    -f {root_folder}/services/postgres/docker-compose.yml \
    -f {root_folder}/services/redis/docker-compose.yml \
    up
"""
    )


services.add_command(cmd=authorisation)
services.add_command(cmd=iot)
services.add_command(cmd=postgres)
services.add_command(cmd=redis)
