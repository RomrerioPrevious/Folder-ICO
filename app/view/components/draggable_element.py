from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QLabel


class DraggableElement(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._dragging = False
        self._drag_start_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_start_pos = event.pos()
            self.raise_()  # Выводит элемент на передний план

    def mouseMoveEvent(self, event):
        if self._dragging:
            new_pos = self.mapToParent(event.pos() - self._drag_start_pos)
            # Ограничение движения
            p_rect = self.parent().rect()
            new_pos.setX(max(0, min(new_pos.x(), p_rect.width() - self.width())))
            new_pos.setY(max(0, min(new_pos.y(), p_rect.height() - self.height())))
            self.move(new_pos)
            # ИСПРАВЛЕНИЕ: Принудительная перерисовка родителя для обновления линии
            self.parent().update()

    def mouseReleaseEvent(self, event):
        self._dragging = False
