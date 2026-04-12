from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from qfluentwidgets import SegmentedWidget, SubtitleLabel


class RightEditorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 20)

        # Навигация
        self.pivot = SegmentedWidget(self)
        self.stacked_widget = QStackedWidget(self)

        # Страницы (Плейсхолдеры)
        self.edit_page = SubtitleLabel("Edit Settings", self)
        self.presets_page = SubtitleLabel("Presets Library", self)

        self.stacked_widget.addWidget(self.edit_page)
        self.stacked_widget.addWidget(self.presets_page)

        self.pivot.addItem("edit", "✏️ Edit", lambda: self.stacked_widget.setCurrentIndex(0))
        self.pivot.addItem("presets", "= Presets", lambda: self.stacked_widget.setCurrentIndex(1))

        self.layout.addWidget(self.pivot)
        self.layout.addWidget(self.stacked_widget, 1, Qt.AlignmentFlag.AlignCenter)
