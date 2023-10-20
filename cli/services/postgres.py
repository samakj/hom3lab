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
