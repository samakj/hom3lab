import click

from services.postgres import postgres


@click.group()
def services() -> None:
    pass


services.add_command(cmd=postgres)
