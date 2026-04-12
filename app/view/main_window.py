from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import NavigationItemPosition, FluentWindow
from qfluentwidgets import FluentIcon as FIF
from .frames import FluentFrame
from .style import StyleSheet
from .scenes import EditScene, SettingsScene
from app.config import CONFIG, CURRENT_LANG


class MainWindow(FluentWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editInterface = FluentFrame("Edit Interface", self, EditScene)
        self.recentInterface = FluentFrame("Recent Interface", self)
        self.donateInterface = FluentFrame("Donate Interface", self)
        self.settingInterface = FluentFrame("Setting Interface", self, SettingsScene)

        StyleSheet.WINDOW.apply(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        lang = CURRENT_LANG["left_navigation"]

        self.addSubInterface(self.editInterface, FIF.EDIT, lang["edit"])
        self.addSubInterface(self.recentInterface, FIF.SAVE, lang["recent"])

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.donateInterface, FIF.MARKET, lang["donate"])

        self.addSubInterface(self.settingInterface, FIF.SETTING, lang["settings"], NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.setFixedSize(1200, 600)
        self.center_window()
        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))
        self.setWindowTitle(CONFIG["app"]["title"])

    def center_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        window_geometry = self.frameGeometry()

        center_point = screen_geometry.center()

        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft())
