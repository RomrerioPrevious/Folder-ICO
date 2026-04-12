from pathlib import Path
import logging
import json


def get_global_path(path: str = None) -> Path | None:
    markers = {"pyproject.toml", ".gitignore", "README.md"}

    current_path = Path(__file__).resolve()

    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in markers):
            if path is not None:
                parent = parent.joinpath(path)
                return parent
            return parent
    return None


GLOBAL_PATH = get_global_path()
GLOBAL_CONFIG_PATH = get_global_path("resources/config.json")

with open(GLOBAL_CONFIG_PATH, "r", encoding="UTF-8") as file:
    CONFIG = json.load(file)

APP_CONFIG = CONFIG["app"]
SETTINGS_CONFIG = CONFIG["app"]["settings"]["custom"]
PATH_CONFIG = CONFIG["path"]["custom"]

GLOBAL_RESOURCE_PATH = get_global_path(PATH_CONFIG["resource"])
GLOBAL_FOLDER_PRESETS_PATH = get_global_path(PATH_CONFIG["folder-presets"])
GLOBAL_LOG_PATH = get_global_path(PATH_CONFIG["logs"])
GLOBAL_LANG_PATH = get_global_path(PATH_CONFIG["lang"])

with open(GLOBAL_LANG_PATH, "r", encoding="UTF-8") as file:
    LANG = json.load(file)

try:
    CURRENT_LANG = LANG[SETTINGS_CONFIG["lang"]]
except KeyError:
    CURRENT_LANG = LANG["eng"]

logging.basicConfig(
    level=logging.INFO, filename=GLOBAL_LOG_PATH.joinpath("logs.log"), filemode="a",
    datefmt='%Y-%m-%d %H:%M:%S',
    format="%(asctime)s %(levelname)s | %(message)s",
    encoding="utf-8"
)
