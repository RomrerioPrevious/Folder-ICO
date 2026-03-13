from app.models import Folder, FolderColor, FolderIcon
import app.utils.checks as checks
from app.exceptions import *
from app.config import *
from PIL import Image, ImageChops, ImageDraw


def draw_frame(img: Image, color: FolderColor, color_layer: Image) -> Image:
    r, g, b, alpha = img.split()
    rgb_template = Image.merge("RGB", (r, g, b))
    colored_texture = ImageChops.multiply(color_layer, rgb_template)

    result = Image.merge("RGBA", (
        colored_texture.getchannel('R'),
        colored_texture.getchannel('G'),
        colored_texture.getchannel('B'),
        alpha
    ))
    return result


def draw_gradient(img: Image, color: FolderColor) -> Image:
    gradient_layer = Image.new("RGB", img.size, color.color1)
    draw = ImageDraw.Draw(gradient_layer)

    p1 = color.start_gradient
    p2 = color.end_gradient

    width = img.size[0]
    height = img.size[1]

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist_sq = dx ** 2 + dy ** 2

    if dist_sq == 0:
        gradient_layer = Image.new("RGB", (width, height), color.color1)
    else:
        c1 = color.color1
        c2 = color.color2

        dr = c2[0] - c1[0]
        dg = c2[1] - c1[1]
        db = c2[2] - c1[2]

        for y in range(height):
            for x in range(width):
                u = ((x - p1[0]) * dx + (y - p1[1]) * dy) / dist_sq
                u = max(0, min(1, u))

                r = int(c1[0] + dr * u)
                g = int(c1[1] + dg * u)
                b = int(c1[2] + db * u)

                draw.point((x, y), fill=(r, g, b))
    return draw_frame(img, color, gradient_layer)


def draw_monochrome(img: Image, color: FolderColor) -> Image:
    color_layer = Image.new("RGB", img.size, color.color1)
    return draw_frame(img, color, color_layer)


def draw_icon_part(style: str, type: str, color: FolderColor) -> Image:
    path = GLOBAL_FOLDER_PRESETS_PATH.joinpath(style, f"{type}.png")
    if not path.exists():
        raise NotFoundIconPart(style, type)

    img = Image.open(path)
    if color.is_gradient:
        return draw_gradient(img, color)
    return draw_monochrome(img, color)


def draw_folder_icon(icon: FolderIcon | None, size: tuple[int, int]) -> Image:
    if icon is None:
        return None

    icon_img = Image.open(icon.icon_path)
    new_width = int(icon_img.width * icon.icon_size)
    new_height = int(icon_img.height * icon.icon_size)
    icon_img = icon_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    result = Image.new("RGBA", size, (0, 0, 0, 0))

    result.paste(icon_img, icon.icon_cords, icon_img)
    return result


def combine_parts(*args) -> Image:
    img = args[0]
    for arg in args[1:]:
        if arg is None:
            continue
        img = Image.alpha_composite(img, arg)
    return img


def render(folder: Folder) -> Image:
    if not checks.folder_style_exists(folder.folder_style):
        raise NotFoundFolderStyle(folder.folder_style)

    main_img = draw_icon_part(folder.folder_style, "main", folder.main_color)
    background_img = draw_icon_part(folder.folder_style, "background", folder.background_color)
    icon_img = draw_folder_icon(folder.icon, main_img.size)

    return combine_parts(main_img, background_img, icon_img)
