import click
from services import services


@click.group()
def cli() -> None:
    pass


cli.add_command(cmd=services)
