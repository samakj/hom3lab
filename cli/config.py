import json
import os
from pathlib import Path
from typing import Any, Union

file = Path(os.path.abspath(__file__))
root_folder = file.parent.parent


def load_json_file(path: Union[Path, str]) -> Any:
    with open(path) as file:
        return json.loads(file.read())


def load_json_config_file(path: Union[Path, str]) -> Any:
    with open(root_folder / "config" / path) as file:
        return json.loads(file.read())


def flattern_dict(obj: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    prefix = f"{prefix}." if prefix else ""
    flattened: dict[str, Any] = {}

    for key, value in obj.items():
        if isinstance(value, dict):
            flattened = {**flattened, **flattern_dict(value, f"{prefix}{key}")}
        else:
            flattened[f"{prefix}{key}"] = value

    return flattened


def load_db_config() -> dict[str, Any]:
    return load_json_config_file("db.json")


def load_flat_db_config() -> dict[str, Any]:
    return flattern_dict(load_db_config(), prefix="db")


def load_secrets_config() -> dict[str, Any]:
    return load_json_config_file("secrets.json")


def load_flat_secrets_config() -> dict[str, Any]:
    return flattern_dict(load_secrets_config(), prefix="secrets")


def apply_configs(
    input_path: Union[Path, str],
    output_path: Union[Path, str],
    template_prefix: str = "",
    template_suffix: str = "",
    extra_config: dict[str, any] = {},
) -> None:
    output_text = ""

    if not input_path.exists():
        raise ValueError(f"Path does not exist: {input_path}")

    with open(file=input_path, mode="r") as input_file:
        output_text = input_file.read()

    for key, value in load_flat_db_config().items():
        output_text = output_text.replace(
            f"{template_prefix}{key}{template_suffix}", str(value)
        )

    for key, value in load_flat_secrets_config().items():
        output_text = output_text.replace(
            f"{template_prefix}{key}{template_suffix}", str(value)
        )

    for key, value in flattern_dict(extra_config).items():
        output_text = output_text.replace(
            f"{template_prefix}{key}{template_suffix}", str(value)
        )

    with open(file=output_path, mode="w") as output_file:
        output_file.write(output_text)
