from app.models import Folder, FolderColor
from PIL import Image


def draw_gradient(img: Image, colors: FolderColor) -> Image:
    ...


def draw_monochrome(img: Image, colors: FolderColor) -> Image:
    ...


def draw_icon_part(img: Image, color: FolderColor):
    if color.is_gradient:
        return draw_gradient(img, color)
    return draw_monochrome(img, color)


def render(folder: Folder):
    ...
