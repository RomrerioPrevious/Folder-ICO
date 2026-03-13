from dataclasses import dataclass


@dataclass
class FolderIcon:
    icon_path: str
    icon_cords: tuple[int, int]
    icon_size: float
