from app.service.render_service import *
from PIL import Image
import copy
import unittest


class RenderServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_path = GLOBAL_PATH.joinpath("tests")
        cls.fixtures_path = cls.test_path.joinpath("fixtures")
        cls.main_color = FolderColor(color1=(60, 219, 137), color2=(70, 208, 181), start_gradient=[0, 0], end_gradient=[200, 200])
        cls.background_color = FolderColor(color1=(7, 49, 65))
        cls.icon = FolderIcon(icon_path=cls.fixtures_path.joinpath("icon.png").__str__(), icon_cords=(82, 95), icon_size=0.75)
        cls.folder = Folder(
            name="test",
            folder_style="win11",
            icon=cls.icon,
            main_color=cls.main_color,
            background_color=cls.background_color,
            frame_color=None,
        )

    def test_not_found_folder_style(self):
        exception_folder = copy.deepcopy(self.folder)
        exception_folder.folder_style = "EXCEPTION_FOLDER_STYLE"

        with self.assertRaises(NotFoundFolderStyle):
            render(exception_folder)

    def test_render(self):
        correct_icon = Image.open(self.fixtures_path.joinpath("correct_icon.png"))
        icon = render(self.folder)

        assert ImageChops.difference(icon, correct_icon).getbbox() is None
