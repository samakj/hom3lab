import click
import os
from pathlib import Path

from config import root_folder, apply_configs


@click.group()
def iot() -> None:
    pass


@iot.command()
def link_shared() -> None:
    os.system(
        f"""
ln -s \
    {root_folder / "shared"} \
    {root_folder / "services/iot/api/shared"} \
        """
    )

@iot.command()
def freeze_requirements() -> None:
    os.chdir(root_folder / "services/iot/api")
    os.system(
        """
python3 -m venv .venv;
. .venv/bin/activate;
pip install -r requirements-to-freeze.txt;
pip freeze > requirements.txt;
deactivate;
        """
    )

@iot.command()
def run_in_venv() -> None:
    os.chdir(root_folder / "services/iot/api")
    os.system(
        f"""
python3 -m venv .venv;
. .venv/bin/activate;
uvicorn main:app --reload --port=8080;
deactivate;
        """
    )


@iot.command()
def build_config() -> None:
    input_path = root_folder / "services/iot/api/config.template.json"
    output_path = root_folder / "services/iot/api/config.json"

    apply_configs(
        input_path=input_path,
        output_path=output_path,
        template_prefix="{",
        template_suffix="}",
    )
    print(f"iot | config.json built.")


@iot.command()
def build_docker_compose() -> None:
    input_path = root_folder / "services/iot/api/docker-compose.template.yml"
    output_path = root_folder / "services/iot/api/docker-compose.yml"

    apply_configs(
        input_path=input_path,
        output_path=output_path,
        template_prefix="{",
        template_suffix="}",
    )
    print(f"iot | docker-compose.yml built.")


@iot.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    build_config.invoke(ctx=ctx)
    build_docker_compose.invoke(ctx=ctx)
