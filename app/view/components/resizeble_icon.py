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
        # Временная заглушка стиля, чтобы видеть элемент
        self.setStyleSheet("background-color: rgba(0, 120, 212, 50); border: 1px solid #0078d4;")

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
            # globalPosition() точнее для перетаскивания
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

        # Базовые координаты исходного прямоугольника
        l0, t0 = self._initial_geometry.left(), self._initial_geometry.top()
        r0, b0 = self._initial_geometry.right(), self._initial_geometry.bottom()
        w0, h0 = self._initial_geometry.width(), self._initial_geometry.height()

        # 1. Вычисляем "сырые" координаты на основе дельты, определяя, что движется
        # Координаты raw_left и т.д. могут временно нарушать логику (left > right),
        # это необходимо для сохранения возможности инверсии.
        raw_left = l0 + delta.x() if "left" in self._resize_handle else l0
        raw_top = t0 + delta.y() if "top" in self._resize_handle else t0
        raw_right = r0 + delta.x() if "right" in self._resize_handle else r0
        raw_bottom = b0 + delta.y() if "bottom" in self._resize_handle else b0

        raw_w = raw_right - raw_left
        raw_h = raw_bottom - raw_top

        # 2. Обработка Shift (сохранение пропорций)
        if QApplication.keyboardModifiers() == Qt.KeyboardModifier.ShiftModifier:
            # Вычисляем целевые абсолютные размеры по минимальной стороне
            abs_w = abs(raw_w)
            abs_h = abs(raw_h)

            if abs_w < abs_h * self._aspect_ratio:
                abs_h = abs_w / self._aspect_ratio
            else:
                abs_w = abs_h * self._aspect_ratio

            # Восстанавливаем знаки (направление) сырых размеров
            raw_w = abs_w if raw_w >= 0 else -abs_w
            raw_h = abs_h if raw_h >= 0 else -abs_h

            # 3. Корректируем координаты, фиксируя противоположную сторону
            # Если тянем LEFT, фиксируем RIGHT: raw_left = raw_right - raw_w
            if "left" in self._resize_handle:
                raw_left = raw_right - raw_w
            else: # тянем RIGHT, фиксируем LEFT (дефолт)
                raw_right = raw_left + raw_w

            # Если тянем TOP, фиксируем BOTTOM: raw_top = raw_bottom - raw_h
            if "top" in self._resize_handle:
                raw_top = raw_bottom - raw_h
            else: # тянем BOTTOM, фиксируем TOP (дефолт)
                raw_bottom = raw_top + raw_h

        # 4. Финальный прямоугольник через QRect(topLeft, QSize).normalized()
        # normalized() корректно обрабатывает отрицательные W/H, меняя местами углы при инверсии
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
            # Акцентный цвет Fluent (Windows 11)
            painter.setBrush(QColor("#0078d4"))
            for rect in self._get_handles().values():
                painter.drawRoundedRect(rect, 2, 2)