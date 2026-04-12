from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import CommandBar, Action, FluentIcon

from app.view.scenes.edit.presets.preview_area import PreviewArea


class LeftEditorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 25, 0, 0)
        self.layout.setSpacing(0)

        # CommandBar
        self.command_bar = CommandBar(self)
        self.init_actions()
        self.command_bar.setFixedWidth(200)
        # Центрирование CommandBar
        self.layout.addWidget(self.command_bar, 0, Qt.AlignmentFlag.AlignHCenter)


        # Зона превью
        self.preview_area = PreviewArea(self)
        self.layout.addWidget(self.preview_area, 1)

    def init_actions(self):
        self.command_bar.addAction(Action(FluentIcon.SAVE, "Сохранить", self))
        self.command_bar.addSeparator()
        self.command_bar.addAction(Action(FluentIcon.ADD, "Добавить иконку", self))
        self.command_bar.addAction(Action(FluentIcon.TAG, "Тип иконки", self))
