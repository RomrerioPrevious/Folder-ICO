from pathlib import Path
import json


def get_global_path() -> Path | None:
    markers = {"pyproject.toml", ".gitignore", "README.md"}

    current_path = Path(__file__).resolve()

    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in markers):
            return parent
    return None


GLOBAL_PATH = get_global_path()
GLOBAL_RESOURCE_PATH = get_global_path().joinpath("resources")
GLOBAL_CONFIG_PATH = get_global_path().joinpath("resources", "config.json")

with open(GLOBAL_CONFIG_PATH, "r", encoding="UTF-8") as file:
    CONFIG = json.load(file)
