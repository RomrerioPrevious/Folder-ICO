from app.config import *


def folder_style_exists(folder_style: str) -> bool:
    paths = [str(item.stem) for item in GLOBAL_FOLDER_PRESETS_PATH.rglob("*") if item.is_dir()]
    return folder_style in paths