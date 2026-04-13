from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt6.QtWidgets import QFrame, QLabel

from app.view.components import DraggableElement, ResizableIcon


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

        # Плейсхолдер картинки
        self.img_placeholder = ResizableIcon(self)
        self.img_placeholder.setStyleSheet("""
                            ResizableIcon {
                                background: rgba(0, 120, 212, 0.1);
                                border: 1px solid rgba(0, 120, 212, 0.3);
                                border-radius: 4px;
                                color: #0078d4;
                                font-weight: bold;
                            }
                        """)
        self.img_placeholder.setText("IMG")
        self.img_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_placeholder.move(50, 50)

        # Точки (Круги)
        self.point_a = DraggableElement(self)
        self.point_b = DraggableElement(self)
        for p in [self.point_a, self.point_b]:
            p.setFixedSize(point_size, point_size)
            # Контур 4px по ТЗ
            p.setStyleSheet(
                f"background: white; border: {self.line_width}px solid gray; border-radius: {point_size // 2}px;")

        self.point_a.move(50, 150)
        self.point_b.move(220, 150)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.show_controls:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            # Линия 4px по ТЗ
            pen = QPen(QColor(128, 128, 128), self.line_width)
            painter.setPen(pen)
            painter.drawLine(self.point_a.geometry().center(),
                             self.point_b.geometry().center())

    def resizeEvent(self, event):
        self.folder_back.move(self.width() // 2 - 150, self.height() // 2 - 125)
