class NotFoundFolderStyle(Exception):
    def __init__(self, folder_style: str = None):
        self.folder_style = folder_style

    def __str__(self):
        if self.folder_style is None:
            return "Folder style not found"
        return f"Folder style {self.folder_style} not found"


class NotFoundIconPart(Exception):
    def __init__(self, style: str = None, type: str = None):
        self.type = type
        self.style = style

    def __str__(self):
        if self.type is None:
            return "Icon part not found"
        return f"Icon part {self.style}, {self.type} not found"
