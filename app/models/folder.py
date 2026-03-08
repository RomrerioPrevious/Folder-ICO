from dataclasses import dataclass
from .folder_color import FolderColor


@dataclass
class Folder:
    name: str
    folder_style: str

    icon_path: str
    icon_cords: [int, int]
    icon_size: [int, int]

    main_color: FolderColor
    background_color: FolderColor
    frame_color: FolderColor
