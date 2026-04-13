
from PyQt6.QtCore import Qt, QPoint, QRect, QSize
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QLabel, QApplication


# Рефакторинг: переместить в ui/components/resizable_icon.py
class ResizableIcon(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self._dragging = False
        self._resizing = False
        self._resize_handle = None

        self._drag_start_pos = QPoint()
        self._initial_geometry = QRect()

        self._handle_size = 8
        self._hovering = False
        self._aspect_ratio = 1.0

        # Убраны минимальные размеры для плавной инверсии
        self.resize(80, 80)

    def _get_handles(self) -> dict:
        w, h = self.width(), self.height()
        s = self._handle_size
        return {
            "top_left": QRect(0, 0, s, s),
            "top_right": QRect(w - s, 0, s, s),
            "bottom_left": QRect(0, h - s, s, s),
            "bottom_right": QRect(w - s, h - s, s, s),
        }

    def enterEvent(self, event):
        self._hovering = True
        self.update()

    def leaveEvent(self, event):
        self._hovering = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self._drag_start_pos = event.globalPosition().toPoint()
            self._initial_geometry = self.geometry()
            self.raise_()

            handles = self._get_handles()
            for name, rect in handles.items():
                if rect.contains(pos):
                    self._resizing = True
                    self._resize_handle = name
                    self._aspect_ratio = self.width() / self.height() if self.height() != 0 else 1.0
                    return

            self._dragging = True

    def mouseMoveEvent(self, event):
        pos = event.pos()
        global_pos = event.globalPosition().toPoint()
        handles = self._get_handles()

        if not self._resizing and not self._dragging:
            if "top_left" in handles and (handles["top_left"].contains(pos) or handles["bottom_right"].contains(pos)):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif "top_right" in handles and (
                    handles["top_right"].contains(pos) or handles["bottom_left"].contains(pos)):
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

        if self._dragging:
            delta = global_pos - self._drag_start_pos
            new_pos = self._initial_geometry.topLeft() + delta
            self._move_with_constraints(new_pos)
        elif self._resizing:
            self._perform_resize(global_pos)

    def _move_with_constraints(self, new_pos: QPoint):
        p_rect = self.parent().rect()
        x = max(0, min(new_pos.x(), p_rect.width() - self.width()))
        y = max(0, min(new_pos.y(), p_rect.height() - self.height()))
        self.move(x, y)
        if self.parent():
            self.parent().update()

    def _perform_resize(self, global_pos: QPoint):
        delta = global_pos - self._drag_start_pos

        left, top = self._initial_geometry.left(), self._initial_geometry.top()
        right, bottom = self._initial_geometry.right(), self._initial_geometry.bottom()

        if "right" in self._resize_handle: right += delta.x()
        if "left" in self._resize_handle: left += delta.x()
        if "bottom" in self._resize_handle: bottom += delta.y()
        if "top" in self._resize_handle: top += delta.y()

        raw_w = right - left
        raw_h = bottom - top

        if QApplication.keyboardModifiers() == Qt.KeyboardModifier.ShiftModifier:
            sign_w = 1 if raw_w >= 0 else -1
            sign_h = 1 if raw_h >= 0 else -1

            abs_w = abs(raw_w)
            abs_h = abs_w / self._aspect_ratio

            raw_w = abs_w * sign_w
            raw_h = abs_h * sign_h

        # Инверсия происходит здесь: normalized() корректно обрабатывает отрицательные размеры
        final_rect = QRect(QPoint(left, top), QSize(int(raw_w), int(raw_h))).normalized()

        if self.parent().rect().contains(final_rect):
            self.setGeometry(final_rect)
            self.parent().update()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self._resizing = False
        self._resize_handle = None

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._hovering:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(Qt.PenStyle.NoPen)
            # Использование акцентного цвета Fluent (Windows 11)
            painter.setBrush(QColor("#0078d4"))
            for rect in self._get_handles().values():
                painter.drawRoundedRect(rect, 2, 2)