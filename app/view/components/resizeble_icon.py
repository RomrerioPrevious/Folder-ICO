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

        self.resize(80, 80)
        self.setStyleSheet("background-color: rgba(0, 120, 212, 50); border: 1px solid #0078d4;")

    def _get_handles(self) -> dict:
        w, h = self.width(), self.height()
        s = self._handle_size
        m_w, m_h = w // 2 - s // 2, h // 2 - s // 2

        return {
            # Углы
            "top_left": QRect(0, 0, s, s),
            "top_right": QRect(w - s, 0, s, s),
            "bottom_left": QRect(0, h - s, s, s),
            "bottom_right": QRect(w - s, h - s, s, s),
            # Стороны
            "top": QRect(m_w, 0, s, s),
            "bottom": QRect(m_w, h - s, s, s),
            "left": QRect(0, m_h, s, s),
            "right": QRect(w - s, m_h, s, s),
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
            self._update_cursor(pos, handles)

        if self._dragging:
            delta = global_pos - self._drag_start_pos
            new_pos = self._initial_geometry.topLeft() + delta
            self._move_with_constraints(new_pos)
        elif self._resizing:
            self._perform_resize(global_pos)

    def _update_cursor(self, pos, handles):
        if handles["top_left"].contains(pos) or handles["bottom_right"].contains(pos):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif handles["top_right"].contains(pos) or handles["bottom_left"].contains(pos):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif handles["top"].contains(pos) or handles["bottom"].contains(pos):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif handles["left"].contains(pos) or handles["right"].contains(pos):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _move_with_constraints(self, new_pos: QPoint):
        if not self.parent():
            self.move(new_pos)
            return

        p_rect = self.parent().rect()
        x = max(0, min(new_pos.x(), p_rect.width() - self.width()))
        y = max(0, min(new_pos.y(), p_rect.height() - self.height()))
        self.move(x, y)
        self.parent().update()

    def _perform_resize(self, global_pos: QPoint):
        delta = global_pos - self._drag_start_pos
        l0, t0 = self._initial_geometry.left(), self._initial_geometry.top()
        r0, b0 = self._initial_geometry.right(), self._initial_geometry.bottom()

        # Определение сырых координат
        raw_left = l0 + delta.x() if "left" in self._resize_handle else l0
        raw_top = t0 + delta.y() if "top" in self._resize_handle else t0
        raw_right = r0 + delta.x() if "right" in self._resize_handle else r0
        raw_bottom = b0 + delta.y() if "bottom" in self._resize_handle else b0

        # Коррекция пропорций (Shift)
        if QApplication.keyboardModifiers() == Qt.KeyboardModifier.ShiftModifier:
            raw_w, raw_h = raw_right - raw_left, raw_bottom - raw_top
            abs_w, abs_h = abs(raw_w), abs(raw_h)

            if abs_w < abs_h * self._aspect_ratio:
                abs_h = abs_w / self._aspect_ratio
            else:
                abs_w = abs_h * self._aspect_ratio

            raw_w = abs_w if raw_w >= 0 else -abs_w
            raw_h = abs_h if raw_h >= 0 else -abs_h

            if "left" in self._resize_handle:
                raw_left = raw_right - raw_w
            else:
                raw_right = raw_left + raw_w

            if "top" in self._resize_handle:
                raw_top = raw_bottom - raw_h
            else:
                raw_bottom = raw_top + raw_h

        final_rect = QRect(
            QPoint(int(raw_left), int(raw_top)),
            QSize(int(raw_right - raw_left), int(raw_bottom - raw_top))
        ).normalized()

        if not self.parent() or self.parent().rect().contains(final_rect):
            self.setGeometry(final_rect)
            if self.parent():
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
            painter.setBrush(QColor("#0078d4"))
            for rect in self._get_handles().values():
                painter.drawRoundedRect(rect, 2, 2)
