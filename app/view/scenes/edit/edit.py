from PyQt6.QtWidgets import (QWidget, QHBoxLayout)
from qfluentwidgets import (HorizontalSeparator)
from app.view.scenes.edit.presets.left_editor_panel import LeftEditorPanel
from app.view.scenes.edit.presets.right_editor_panel import RightEditorPanel


class EditScene(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.left_panel = LeftEditorPanel(self)
        self.right_panel = RightEditorPanel(self)

        self.layout.addWidget(self.left_panel, 1)
        self.layout.addWidget(HorizontalSeparator(self))
        self.layout.addWidget(self.right_panel, 1)
