from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel, setFont


class FluentFrame(QFrame):
    def __init__(self, text: str, parent=None, scene: type[QWidget] = None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)

        if scene is None:
            self.add_placeholder(text)
        else:
            self.scene_instance = scene(self)
            self.main_layout.addWidget(self.scene_instance)

        self.setObjectName(text.replace(" ", "-"))
        self.resize(900, 600)

    def add_placeholder(self, text: str = ""):
        self.label = SubtitleLabel(text, self)
        self.label.resize(900, 600)
        self.label.move(300, 0)
        self.main_layout = QHBoxLayout(self)
        setFont(self.label, 24)

