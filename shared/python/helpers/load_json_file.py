import json
from pathlib import Path
from typing import Any, Union


def load_json_file(path: Union[Path, str]) -> Any:
    with open(path) as file:
        return json.loads(file.read())
