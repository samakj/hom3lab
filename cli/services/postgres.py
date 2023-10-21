import click
import os
from pathlib import Path

from config import root_folder, apply_configs


@click.group()
def postgres() -> None:
    pass


@postgres.command()
def build_patches() -> None:
    build_folder = root_folder / "services/postgres/patches/build"
    templates_folder = root_folder / "services/postgres/patches/templates"

    if not os.path.exists(build_folder):
        os.makedirs(build_folder)

    for folder, _, files in os.walk(templates_folder):
        for file in files:
            input_path = Path(folder) / file
            output_file = str(file).replace(".template", "")
            output_path = build_folder / output_file
            apply_configs(
                input_path=input_path,
                output_path=output_path,
                template_prefix="{",
                template_suffix="}",
            )
            print(f"Postgres | {output_file} built.")


@postgres.command()
def build_docker_compose() -> None:
    input_path = root_folder / "services/postgres/docker-compose.template.yml"
    output_path = root_folder / "services/postgres/docker-compose.yml"

    apply_configs(
        input_path=input_path,
        output_path=output_path,
        template_prefix="{",
        template_suffix="}",
    )
    print(f"Postgres | docker-compose.yml built.")


@postgres.command()
def build_data_folder() -> None:
    path = root_folder / "services/postgres/data"

    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Postgres | data folder created.")
    else:
        print(f"Postgres | data folder already exists.")


@postgres.command()
def build_dumps_folder() -> None:
    path = root_folder / "services/postgres/dumps"

    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Postgres | dumps folder created.")
    else:
        print(f"Postgres | dumps folder already exists.")


@postgres.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    build_patches.invoke(ctx=ctx)
    build_docker_compose.invoke(ctx=ctx)
    build_data_folder.invoke(ctx=ctx)
    build_dumps_folder.invoke(ctx=ctx)
