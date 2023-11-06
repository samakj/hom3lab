from pathlib import Path
from shared.python.helpers.load_json_file import load_json_file

config = load_json_file(Path(__file__).parent / "config.json")
