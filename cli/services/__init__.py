import click

from services.postgres import postgres
from services.redis import redis


@click.group()
def services() -> None:
    pass


services.add_command(cmd=postgres)
services.add_command(cmd=redis)
