import click
import os
from pathlib import Path

from config import root_folder, apply_configs


@click.group()
def authorisation() -> None:
    pass


@authorisation.command()
def link_shared() -> None:
    os.system(
        f"""
ln -s \
    {root_folder / "shared"} \
    {root_folder / "services/authorisation/api/shared"} \
        """
    )


@authorisation.command()
def build_config() -> None:
    input_path = root_folder / "services/authorisation/api/config.template.json"
    output_path = root_folder / "services/authorisation/api/config.json"

    apply_configs(
        input_path=input_path,
        output_path=output_path,
        template_prefix="{",
        template_suffix="}",
    )
    print(f"Authorisation | config.json built.")


@authorisation.command()
def build_docker_compose() -> None:
    input_path = root_folder / "services/authorisation/api/docker-compose.template.yml"
    output_path = root_folder / "services/authorisation/api/docker-compose.yml"

    apply_configs(
        input_path=input_path,
        output_path=output_path,
        template_prefix="{",
        template_suffix="}",
    )
    print(f"Authorisation | docker-compose.yml built.")


@authorisation.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    build_config.invoke(ctx=ctx)
    build_docker_compose.invoke(ctx=ctx)
