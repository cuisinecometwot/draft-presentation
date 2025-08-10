#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QColorDialog
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap, QFont, QKeySequence, QShortcut

class DrawingOverlay(QWidget):
    def __init__(self, target_widget, pan_offset=QPoint(0, 0)):
        super().__init__()
        self.target_widget = target_widget
        self.pan_offset = pan_offset
        
        # Thiết lập overlay
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        
        # Biến vẽ
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = QColor(255, 0, 0)  # Màu đỏ mặc định
        self.pen_width = 3
        self.drawing_history = []
        self.current_drawing = []
        
        # Tạo canvas vẽ
        self.canvas = QPixmap(target_widget.size())
        self.canvas.fill(Qt.GlobalColor.transparent)
        
        # Thiết lập giao diện
        self.init_ui()
        self.setup_shortcuts()
        
        # Cập nhật vị trí và kích thước
        self.update_position()
        
    def set_pan_offset(self, pan_offset):
        """Cập nhật pan offset"""
        self.pan_offset = pan_offset
        self.update_canvas()
        
    def init_ui(self):
        # Layout chính
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Thanh công cụ vẽ
        self.toolbar = self.create_toolbar()
        layout.addWidget(self.toolbar)
        
        # Khu vực vẽ (chiếm toàn bộ không gian còn lại)
        self.drawing_area = QLabel()
        self.drawing_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drawing_area.setMinimumSize(1, 1)  # Đảm bảo có kích thước tối thiểu
        layout.addWidget(self.drawing_area)
        
        # Cập nhật canvas
        self.update_canvas()
        
    def create_toolbar(self):
        toolbar = QWidget()
        toolbar.setFixedHeight(50)  # Sử dụng fixed height thay vì maximum
        toolbar.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 5px;
                margin: 5px;
            }
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Nút xóa
        self.clear_btn = QPushButton("Xóa")
        self.clear_btn.clicked.connect(self.clear_drawing)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        # Nút hoàn tác
        self.undo_btn = QPushButton("Hoàn tác")
        self.undo_btn.clicked.connect(self.undo_last_drawing)
        self.undo_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        
        # Nút thay đổi màu
        self.color_btn = QPushButton("Màu")
        self.color_btn.clicked.connect(self.change_color)
        self.color_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        # Thanh trượt độ dày nét vẽ
        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.width_slider.setRange(1, 20)
        self.width_slider.setValue(3)
        self.width_slider.valueChanged.connect(self.change_pen_width)
        self.width_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 10px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #007bff;
                border: 1px solid #007bff;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)
        
        # Label độ dày
        width_label = QLabel("Độ dày:")
        width_label.setStyleSheet("color: white; font-size: 12px;")
        
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.undo_btn)
        layout.addWidget(self.color_btn)
        layout.addWidget(width_label)
        layout.addWidget(self.width_slider)
        layout.addStretch()
        
        return toolbar
        
    def setup_shortcuts(self):
        # Phím tắt
        self.shortcut_clear = QShortcut(QKeySequence("Delete"), self)
        self.shortcut_clear.activated.connect(self.clear_drawing)
        
        self.shortcut_undo = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut_undo.activated.connect(self.undo_last_drawing)
        
        self.shortcut_color = QShortcut(QKeySequence("C"), self)
        self.shortcut_color.activated.connect(self.change_color)
        
    def update_position(self):
        """Cập nhật vị trí overlay để khớp với target widget"""
        if self.target_widget:
            pos = self.target_widget.mapToGlobal(self.target_widget.rect().topLeft())
            size = self.target_widget.size()
            self.setGeometry(pos.x(), pos.y(), size.width(), size.height())
            
    def update_canvas(self):
        """Cập nhật canvas vẽ"""
        if self.target_widget:
            # Tạo canvas với kích thước của target widget (không bao gồm toolbar)
            target_size = self.target_widget.size()
            self.canvas = QPixmap(target_size)
            self.canvas.fill(Qt.GlobalColor.transparent)
            
            # Vẽ lại tất cả các nét vẽ
            painter = QPainter(self.canvas)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            for drawing_path in self.drawing_history:
                pen = QPen(drawing_path['color'], drawing_path['width'])
                painter.setPen(pen)
                
                points = drawing_path['points']
                if len(points) > 1:
                    for i in range(1, len(points)):
                        painter.drawLine(points[i-1], points[i])
                        
            painter.end()
            
            # Hiển thị canvas
            self.drawing_area.setPixmap(self.canvas)
            
    def mousePressEvent(self, event):
        """Xử lý sự kiện nhấn chuột"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            # Tính toán vị trí tương đối với khu vực vẽ (không bao gồm toolbar)
            pos = event.pos()
            toolbar_height = self.toolbar.height()
            relative_pos = QPoint(pos.x(), pos.y() - toolbar_height)
            
            # Điều chỉnh vị trí theo pan offset
            adjusted_pos = relative_pos - self.pan_offset
            
            # Đảm bảo vị trí nằm trong khu vực vẽ
            if adjusted_pos.y() >= 0:
                self.last_point = adjusted_pos
                self.current_drawing = [adjusted_pos]
            
    def mouseMoveEvent(self, event):
        """Xử lý sự kiện di chuyển chuột"""
        if self.drawing:
            # Tính toán vị trí tương đối với khu vực vẽ (không bao gồm toolbar)
            pos = event.pos()
            toolbar_height = self.toolbar.height()
            relative_pos = QPoint(pos.x(), pos.y() - toolbar_height)
            
            # Điều chỉnh vị trí theo pan offset
            current_point = relative_pos - self.pan_offset
            
            # Chỉ vẽ nếu vị trí nằm trong khu vực vẽ
            if current_point.y() >= 0 and self.last_point.y() >= 0:
                # Vẽ lên canvas
                painter = QPainter(self.canvas)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                pen = QPen(self.pen_color, self.pen_width)
                painter.setPen(pen)
                painter.drawLine(self.last_point, current_point)
                painter.end()
                
                # Lưu điểm để vẽ
                self.current_drawing.append(current_point)
                
                # Cập nhật hiển thị
                self.drawing_area.setPixmap(self.canvas)
                
                self.last_point = current_point
            
    def mouseReleaseEvent(self, event):
        """Xử lý sự kiện thả chuột"""
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            
            # Lưu nét vẽ vào lịch sử
            if len(self.current_drawing) > 1:
                self.drawing_history.append({
                    'points': self.current_drawing.copy(),
                    'color': QColor(self.pen_color),
                    'width': self.pen_width
                })
                
    def clear_drawing(self):
        """Xóa toàn bộ nét vẽ"""
        self.drawing_history.clear()
        self.canvas.fill(Qt.GlobalColor.transparent)
        self.drawing_area.setPixmap(self.canvas)
        
    def undo_last_drawing(self):
        """Hoàn tác nét vẽ cuối cùng"""
        if self.drawing_history:
            self.drawing_history.pop()
            self.update_canvas()
            
    def change_color(self):
        """Thay đổi màu vẽ"""
        color = QColorDialog.getColor(self.pen_color, self)
        if color.isValid():
            self.pen_color = color
            
    def change_pen_width(self, width):
        """Thay đổi độ dày nét vẽ"""
        self.pen_width = width
        
    def resizeEvent(self, event):
        """Xử lý sự kiện thay đổi kích thước"""
        super().resizeEvent(event)
        self.update_canvas()
        
    def showEvent(self, event):
        """Xử lý sự kiện hiển thị"""
        super().showEvent(event)
        self.update_position()
        
    def get_drawing_image(self):
        """Lấy ảnh của nét vẽ (để lưu hoặc xuất)"""
        return self.canvas
        
    def save_drawing(self, file_path):
        """Lưu nét vẽ thành file ảnh"""
        try:
            self.canvas.save(file_path)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu: {e}")
            return False 