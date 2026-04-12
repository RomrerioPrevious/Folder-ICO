from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt6.QtWidgets import QFrame, QLabel

from app.view.components.draggable_element import DraggableElement


class PreviewArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.show_controls = True

        point_size = 30
        self.line_width = 4

        # Папка
        self.folder_back = QLabel(self)
        self.folder_back.setPixmap(QPixmap(200, 200))
        self.folder_back.setStyleSheet("background-color: rgba(0, 0, 0, 0.05); border-radius: 15px;")
        self.folder_back.setText("Folder View")
        self.folder_back.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.folder_back.resize(300, 250)

        # Точки (Круги)
        self.point_a = DraggableElement(self)
        self.point_b = DraggableElement(self)
        for p in [self.point_a, self.point_b]:
            p.setFixedSize(point_size, point_size)
            # Контур 4px по ТЗ
            p.setStyleSheet(
                f"background: white; border: {self.line_width}px solid black; border-radius: {point_size // 2}px;")

        self.point_a.move(50, 150)
        self.point_b.move(220, 150)

        # Плейсхолдер картинки
        self.img_placeholder = DraggableElement(self)
        self.img_placeholder.setFixedSize(80, 80)
        self.img_placeholder.setStyleSheet("background: rgba(0, 120, 212, 0.2); border: 2px dashed #0078d4;")
        self.img_placeholder.setText("IMG")
        self.img_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_placeholder.move(110, 50)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.show_controls:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            # Линия 4px по ТЗ
            pen = QPen(QColor(0, 0, 0), self.line_width)
            painter.setPen(pen)
            painter.drawLine(self.point_a.geometry().center(),
                             self.point_b.geometry().center())

    def resizeEvent(self, event):
        self.folder_back.move(self.width() // 2 - 150, self.height() // 2 - 125)
