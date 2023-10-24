import click
import os
from pathlib import Path

from config import root_folder, apply_configs


@click.group()
def redis() -> None:
    pass


@redis.command()
def build_config() -> None:
    input_path = root_folder / "services/redis/redis.template.conf"
    output_path = root_folder / "services/redis/redis.conf"

    apply_configs(
        input_path=input_path,
        output_path=output_path,
        template_prefix="{",
        template_suffix="}",
    )
    print(f"redis | redis.conf built.")


@redis.command()
def build_docker_compose() -> None:
    input_path = root_folder / "services/redis/docker-compose.template.yml"
    output_path = root_folder / "services/redis/docker-compose.yml"

    apply_configs(
        input_path=input_path,
        output_path=output_path,
        template_prefix="{",
        template_suffix="}",
    )
    print(f"redis | docker-compose.yml built.")


@redis.command()
def build_data_folder() -> None:
    path = root_folder / "services/redis/data"

    if not os.path.exists(path):
        os.mkdir(path)
        print(f"redis | data folder created.")
    else:
        print(f"redis | data folder already exists.")


@redis.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    build_config.invoke(ctx=ctx)
    build_docker_compose.invoke(ctx=ctx)
    build_data_folder.invoke(ctx=ctx)
