from dataclasses import dataclass
from .folder_color import FolderColor
from .folder_icon import FolderIcon


@dataclass
class Folder:
    name: str
    folder_style: str

    icon: FolderIcon | None

    main_color: FolderColor | None
    background_color: FolderColor | None
    frame_color: FolderColor | None
