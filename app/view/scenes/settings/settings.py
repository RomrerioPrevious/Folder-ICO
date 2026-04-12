from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel, setFont, CommandBar, Action, OptionsSettingCard, qconfig, PushSettingCard, \
    ComboBoxSettingCard
from qfluentwidgets import FluentIcon as FIF

from app import CURRENT_LANG


class SettingsScene(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)

        self.initWindow()

        self.setObjectName("text".replace(" ", "-"))

    def initWindow(self):
        lang = CURRENT_LANG["settings"]

        theme = OptionsSettingCard(
            qconfig.themeMode,
            FIF.BRIGHTNESS,
            lang["theme"]["title"],
            lang["theme"]["description"],
            texts=[
                lang["theme"]["choose"]["light"],
                lang["theme"]["choose"]["dark"],
                lang["theme"]["choose"]["system"]
            ],
        )
        download = PushSettingCard(
            text=lang["download"]["description"],
            icon=FIF.DOWNLOAD,
            title=lang["download"]["title"],
            content="D:/Users/Downloads"
        )
        self.main_layout.addWidget(theme)
        self.main_layout.addWidget(download)
