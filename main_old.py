#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QMessageBox, QSlider, QFrame, QSplitter, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QFont, QKeySequence, QShortcut, QWheelEvent, QMouseEvent
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget

from presentation_viewer import PresentationViewer
from script_window import ScriptWindow
from drawing_overlay import DrawingOverlay
from screen_recorder import ScreenRecorder

class PresentationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng Trình chiếu")
        self.setGeometry(100, 100, 1200, 800)
        
        # Khởi tạo các thành phần
        self.presentation_viewer = None
        self.script_window = None
        self.drawing_overlay = None
        self.screen_recorder = None
        self.current_file = None
        
        # Biến cho tính năng pan
        self.panning = False
        self.last_pan_pos = QPoint()
        self.pan_offset = QPoint(0, 0)
        
        self.init_ui()
        self.setup_shortcuts()
        
    def init_ui(self):
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QVBoxLayout(central_widget)
        
        # Thanh công cụ
        toolbar = self.create_toolbar()
        main_layout.addWidget(toolbar)
        
        # Khu vực trình chiếu với scroll area để hỗ trợ pan
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setMinimumHeight(500)
        
        # Widget chứa presentation
        self.presentation_container = QWidget()
        self.presentation_container.setMinimumSize(1, 1)
        
        # Khu vực trình chiếu
        self.presentation_area = QLabel("Chọn file để trình chiếu")
        self.presentation_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.presentation_area.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 2px dashed #ccc;
                border-radius: 10px;
                font-size: 18px;
                color: #666;
            }
        """)
        self.presentation_area.setMinimumSize(1, 1)
        
        # Layout cho container
        container_layout = QVBoxLayout(self.presentation_container)
        container_layout.addWidget(self.presentation_area)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area.setWidget(self.presentation_container)
        main_layout.addWidget(self.scroll_area)
        
        # Thanh điều khiển
        control_bar = self.create_control_bar()
        main_layout.addWidget(control_bar)
        
    def create_toolbar(self):
        toolbar = QFrame()
        toolbar.setFrameStyle(QFrame.Shape.StyledPanel)
        toolbar.setMaximumHeight(60)
        
        layout = QHBoxLayout(toolbar)
        
        # Nút mở file
        self.open_btn = QPushButton("Mở File")
        self.open_btn.clicked.connect(self.open_file)
        self.open_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Nút mở cửa sổ script
        self.script_btn = QPushButton("Mở Script")
        self.script_btn.clicked.connect(self.toggle_script_window)
        self.script_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        # Nút bật/tắt vẽ
        self.draw_btn = QPushButton("Bật Vẽ")
        self.draw_btn.clicked.connect(self.toggle_drawing)
        self.draw_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        # Nút ghi màn hình
        self.record_btn = QPushButton("Ghi Màn hình")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.record_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        
        # Nút reset zoom
        self.reset_zoom_btn = QPushButton("Reset Zoom")
        self.reset_zoom_btn.clicked.connect(self.reset_zoom)
        self.reset_zoom_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        
        # Nút reset pan
        self.reset_pan_btn = QPushButton("Reset Pan")
        self.reset_pan_btn.clicked.connect(self.reset_pan)
        self.reset_pan_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #455A64;
            }
        """)
        
        layout.addWidget(self.open_btn)
        layout.addWidget(self.script_btn)
        layout.addWidget(self.draw_btn)
        layout.addWidget(self.record_btn)
        layout.addWidget(self.reset_zoom_btn)
        layout.addWidget(self.reset_pan_btn)
        layout.addStretch()
        
        return toolbar
        
    def create_control_bar(self):
        control_bar = QFrame()
        control_bar.setFrameStyle(QFrame.Shape.StyledPanel)
        control_bar.setMaximumHeight(80)
        
        layout = QHBoxLayout(control_bar)
        
        # Nút trước/sau
        self.prev_btn = QPushButton("← Trước")
        self.prev_btn.clicked.connect(self.previous_slide)
        self.prev_btn.setEnabled(False)
        
        self.next_btn = QPushButton("Sau →")
        self.next_btn.clicked.connect(self.next_slide)
        self.next_btn.setEnabled(False)
        
        # Thanh trượt
        self.slide_slider = QSlider(Qt.Orientation.Horizontal)
        self.slide_slider.setEnabled(False)
        self.slide_slider.valueChanged.connect(self.slide_changed)
        
        # Label hiển thị slide hiện tại
        self.slide_label = QLabel("0 / 0")
        self.slide_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Label hiển thị zoom
        self.zoom_label = QLabel("Zoom: 100%")
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_label.setStyleSheet("color: #666; font-size: 12px;")
        
        # Nút fullscreen - đặt gần với các nút điều khiển trang
        self.fullscreen_btn = QPushButton("Toàn màn hình")
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        
        # Sắp xếp lại: nút fullscreen nằm gần với các nút điều khiển trang
        layout.addWidget(self.prev_btn)
        layout.addWidget(self.slide_slider)
        layout.addWidget(self.slide_label)
        layout.addWidget(self.next_btn)
        layout.addWidget(self.zoom_label)
        layout.addWidget(self.fullscreen_btn)
        layout.addStretch()
        
        return control_bar
        
    def setup_shortcuts(self):
        # Phím tắt
        self.shortcut_next = QShortcut(QKeySequence("Right"), self)
        self.shortcut_next.activated.connect(self.next_slide)
        
        self.shortcut_prev = QShortcut(QKeySequence("Left"), self)
        self.shortcut_prev.activated.connect(self.previous_slide)
        
        self.shortcut_fullscreen = QShortcut(QKeySequence("F11"), self)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)
        
        self.shortcut_draw = QShortcut(QKeySequence("D"), self)
        self.shortcut_draw.activated.connect(self.toggle_drawing)
        
        # Phím tắt zoom
        self.shortcut_zoom_in = QShortcut(QKeySequence("Ctrl+="), self)
        self.shortcut_zoom_in.activated.connect(lambda: self.zoom_in())
        
        self.shortcut_zoom_out = QShortcut(QKeySequence("Ctrl+-"), self)
        self.shortcut_zoom_out.activated.connect(lambda: self.zoom_out())
        
        self.shortcut_reset_zoom = QShortcut(QKeySequence("Ctrl+0"), self)
        self.shortcut_reset_zoom.activated.connect(self.reset_zoom)
        
        # Phím tắt reset pan
        self.shortcut_reset_pan = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut_reset_pan.activated.connect(self.reset_pan)
        
    def wheelEvent(self, event: QWheelEvent):
        """Xử lý mouse wheel events"""
        if self.presentation_viewer:
            # Kiểm tra xem có đang giữ Ctrl không
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                # Zoom in/out
                delta = event.angleDelta().y()
                if delta > 0:
                    self.zoom_in()
                else:
                    self.zoom_out()
                self.update_slide_display()
            else:
                # Chuyển trang
                delta = event.angleDelta().y()
                if delta > 0:
                    self.previous_slide()
                else:
                    self.next_slide()
        
        event.accept()
        
    def mousePressEvent(self, event: QMouseEvent):
        """Xử lý sự kiện nhấn chuột"""
        if event.button() == Qt.MouseButton.RightButton:
            self.panning = True
            self.last_pan_pos = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event: QMouseEvent):
        """Xử lý sự kiện di chuyển chuột"""
        if self.panning and self.presentation_viewer:
            current_pos = event.pos()
            delta = current_pos - self.last_pan_pos
            
            # Cập nhật pan offset
            self.pan_offset += delta
            
            # Cập nhật hiển thị slide với pan offset
            self.update_slide_display()
            
            self.last_pan_pos = current_pos
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Xử lý sự kiện thả chuột"""
        if event.button() == Qt.MouseButton.RightButton:
            self.panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)
        
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn file trình chiếu", "", 
            "PDF Files (*.pdf);;PowerPoint Files (*.pptx *.ppt);;All Files (*)"
        )
        
        if file_path:
            self.load_presentation(file_path)
            
    def load_presentation(self, file_path):
        try:
            self.current_file = file_path
            self.presentation_viewer = PresentationViewer(file_path)
            
            # Reset pan offset khi tải file mới
            self.pan_offset = QPoint(0, 0)
            
            # Cập nhật giao diện
            self.update_slide_display()
            self.slide_slider.setMaximum(self.presentation_viewer.get_total_slides() - 1)
            self.slide_slider.setValue(0)
            self.slide_label.setText(f"1 / {self.presentation_viewer.get_total_slides()}")
            
            # Bật các nút điều khiển
            self.prev_btn.setEnabled(True)
            self.next_btn.setEnabled(True)
            self.slide_slider.setEnabled(True)
            
            QMessageBox.information(self, "Thành công", f"Đã tải file: {os.path.basename(file_path)}")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải file: {str(e)}")
            
    def next_slide(self):
        if self.presentation_viewer:
            self.presentation_viewer.next_slide()
            # Reset pan offset khi chuyển slide
            self.pan_offset = QPoint(0, 0)
            self.update_slide_display()
            
    def previous_slide(self):
        if self.presentation_viewer:
            self.presentation_viewer.previous_slide()
            # Reset pan offset khi chuyển slide
            self.pan_offset = QPoint(0, 0)
            self.update_slide_display()
            
    def slide_changed(self, value):
        if self.presentation_viewer:
            self.presentation_viewer.go_to_slide(value)
            # Reset pan offset khi chuyển slide
            self.pan_offset = QPoint(0, 0)
            self.update_slide_display()
            
    def update_slide_display(self):
        if self.presentation_viewer:
            # Lấy kích thước của scroll area (cố định)
            target_size = QSize(self.scroll_area.width(), self.scroll_area.height())
            
            # Lấy slide với fit size và zoom
            slide_pixmap = self.presentation_viewer.get_current_slide(target_size)
            if slide_pixmap:
                # Tạo pixmap mới với kích thước cố định
                display_pixmap = QPixmap(target_size)
                display_pixmap.fill(Qt.GlobalColor.transparent)
                
                # Vẽ slide vào pixmap với pan offset
                painter = QPainter(display_pixmap)
                
                # Tính vị trí để center slide
                x_offset = (target_size.width() - slide_pixmap.width()) // 2 + self.pan_offset.x()
                y_offset = (target_size.height() - slide_pixmap.height()) // 2 + self.pan_offset.y()
                
                painter.drawPixmap(x_offset, y_offset, slide_pixmap)
                painter.end()
                
                self.presentation_area.setPixmap(display_pixmap)
                
                # Cập nhật kích thước container để scroll area hoạt động đúng
                self.presentation_container.setFixedSize(target_size)
                
                # Cập nhật pan offset cho drawing overlay nếu đang hiển thị
                if self.drawing_overlay and self.drawing_overlay.isVisible():
                    self.drawing_overlay.set_pan_offset(self.pan_offset)
                
                # Cập nhật thông tin slide
                current_slide = self.presentation_viewer.get_current_slide_number() + 1
                total_slides = self.presentation_viewer.get_total_slides()
                self.slide_label.setText(f"{current_slide} / {total_slides}")
                self.slide_slider.setValue(self.presentation_viewer.get_current_slide_number())
                
                # Cập nhật thông tin zoom
                zoom_percent = int(self.presentation_viewer.get_zoom_factor() * 100)
                self.zoom_label.setText(f"Zoom: {zoom_percent}%")
                
    def zoom_in(self, factor=1.2):
        """Zoom in slide"""
        if self.presentation_viewer:
            self.presentation_viewer.zoom_in(factor)
            self.update_slide_display()
            
    def zoom_out(self, factor=1.2):
        """Zoom out slide"""
        if self.presentation_viewer:
            self.presentation_viewer.zoom_out(factor)
            self.update_slide_display()
            
    def reset_zoom(self):
        """Reset zoom về mặc định"""
        if self.presentation_viewer:
            self.presentation_viewer.reset_zoom()
            self.update_slide_display()
            
    def reset_pan(self):
        """Reset pan về vị trí mặc định"""
        self.pan_offset = QPoint(0, 0)
        if self.presentation_viewer:
            self.update_slide_display()
            
    def toggle_script_window(self):
        if not self.script_window:
            self.script_window = ScriptWindow()
            self.script_window.show()
        else:
            if self.script_window.isVisible():
                self.script_window.hide()
            else:
                self.script_window.show()
                
    def toggle_drawing(self):
        if not self.drawing_overlay:
            self.drawing_overlay = DrawingOverlay(self.presentation_area, self.pan_offset)
            
        if self.drawing_overlay.isVisible():
            self.drawing_overlay.hide()
            self.draw_btn.setText("Bật Vẽ")
        else:
            # Cập nhật pan offset cho drawing overlay
            if self.drawing_overlay:
                self.drawing_overlay.set_pan_offset(self.pan_offset)
            self.drawing_overlay.show()
            self.draw_btn.setText("Tắt Vẽ")
            
    def toggle_recording(self):
        if not self.screen_recorder:
            self.screen_recorder = ScreenRecorder()
            
        if self.screen_recorder.is_recording():
            self.screen_recorder.stop_recording()
            self.record_btn.setText("Ghi Màn hình")
        else:
            self.screen_recorder.start_recording()
            self.record_btn.setText("Dừng Ghi")
            
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Ứng dụng Trình chiếu")
    
    # Thiết lập style
    app.setStyle('Fusion')
    
    window = PresentationApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 