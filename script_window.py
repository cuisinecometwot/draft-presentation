#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QFileDialog, 
                             QMessageBox, QFontDialog, QColorDialog, QSpinBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette, QKeySequence, QShortcut

class ScriptWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Script Nói")
        self.setGeometry(1300, 100, 400, 600)
        
        # Thiết lập cửa sổ luôn ở trên cùng
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # Biến lưu trữ
        self.script_file = None
        self.current_font = QFont("Arial", 12)
        self.current_color = QColor(0, 0, 0)
        self.auto_scroll = True
        self.scroll_speed = 1
        
        self.init_ui()
        self.setup_shortcuts()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Thanh công cụ
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # Khu vực hiển thị script
        self.script_display = QTextEdit()
        self.script_display.setReadOnly(True)
        self.script_display.setFont(self.current_font)
        self.script_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                line-height: 1.6;
            }
        """)
        layout.addWidget(self.script_display)
        
        # Thanh điều khiển
        control_bar = self.create_control_bar()
        layout.addWidget(control_bar)
        
        # Thiết lập timer cho auto-scroll
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.auto_scroll_text)
        
    def create_toolbar(self):
        toolbar = QWidget()
        toolbar.setMaximumHeight(50)
        
        layout = QHBoxLayout(toolbar)
        
        # Nút mở file script
        self.open_script_btn = QPushButton("Mở Script")
        self.open_script_btn.clicked.connect(self.open_script_file)
        self.open_script_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        # Nút thiết lập font
        self.font_btn = QPushButton("Font")
        self.font_btn.clicked.connect(self.change_font)
        self.font_btn.setStyleSheet("""
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
        
        # Nút thiết lập màu
        self.color_btn = QPushButton("Màu")
        self.color_btn.clicked.connect(self.change_color)
        self.color_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        
        # Checkbox auto-scroll
        from PyQt6.QtWidgets import QCheckBox
        self.auto_scroll_cb = QCheckBox("Tự động cuộn")
        self.auto_scroll_cb.setChecked(self.auto_scroll)
        self.auto_scroll_cb.stateChanged.connect(self.toggle_auto_scroll)
        
        layout.addWidget(self.open_script_btn)
        layout.addWidget(self.font_btn)
        layout.addWidget(self.color_btn)
        layout.addWidget(self.auto_scroll_cb)
        layout.addStretch()
        
        return toolbar
        
    def create_control_bar(self):
        control_bar = QWidget()
        control_bar.setMaximumHeight(60)
        
        layout = QHBoxLayout(control_bar)
        
        # Nút cuộn lên/xuống
        self.scroll_up_btn = QPushButton("↑")
        self.scroll_up_btn.clicked.connect(self.scroll_up)
        self.scroll_up_btn.setMaximumWidth(40)
        
        self.scroll_down_btn = QPushButton("↓")
        self.scroll_down_btn.clicked.connect(self.scroll_down)
        self.scroll_down_btn.setMaximumWidth(40)
        
        # Điều chỉnh tốc độ cuộn
        layout.addWidget(QLabel("Tốc độ:"))
        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setRange(1, 10)
        self.speed_spinbox.setValue(self.scroll_speed)
        self.speed_spinbox.valueChanged.connect(self.change_scroll_speed)
        self.speed_spinbox.setMaximumWidth(60)
        
        # Nút reset về đầu
        self.reset_btn = QPushButton("Về đầu")
        self.reset_btn.clicked.connect(self.reset_to_top)
        
        layout.addWidget(self.scroll_up_btn)
        layout.addWidget(self.scroll_down_btn)
        layout.addWidget(self.speed_spinbox)
        layout.addWidget(self.reset_btn)
        layout.addStretch()
        
        return control_bar
        
    def setup_shortcuts(self):
        # Phím tắt
        self.shortcut_up = QShortcut(QKeySequence("Up"), self)
        self.shortcut_up.activated.connect(self.scroll_up)
        
        self.shortcut_down = QShortcut(QKeySequence("Down"), self)
        self.shortcut_down.activated.connect(self.scroll_down)
        
        self.shortcut_home = QShortcut(QKeySequence("Home"), self)
        self.shortcut_home.activated.connect(self.reset_to_top)
        
        self.shortcut_end = QShortcut(QKeySequence("End"), self)
        self.shortcut_end.activated.connect(self.scroll_to_bottom)
        
    def open_script_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Mở file script", "", 
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                self.script_display.setPlainText(content)
                self.script_file = file_path
                self.setWindowTitle(f"Script Nói - {os.path.basename(file_path)}")
                
                QMessageBox.information(self, "Thành công", "Đã tải script thành công!")
                
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể đọc file: {str(e)}")
                
    def change_font(self):
        font, ok = QFontDialog.getFont(self.current_font, self)
        if ok:
            self.current_font = font
            self.script_display.setFont(font)
            
    def change_color(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            palette = self.script_display.palette()
            palette.setColor(QPalette.ColorRole.Text, color)
            self.script_display.setPalette(palette)
            
    def toggle_auto_scroll(self, state):
        self.auto_scroll = bool(state)
        if self.auto_scroll:
            self.scroll_timer.start(100)  # Cập nhật mỗi 100ms
        else:
            self.scroll_timer.stop()
            
    def change_scroll_speed(self, value):
        self.scroll_speed = value
        
    def auto_scroll_text(self):
        if self.auto_scroll:
            # Cuộn xuống từ từ
            scrollbar = self.script_display.verticalScrollBar()
            current_pos = scrollbar.value()
            max_pos = scrollbar.maximum()
            
            if current_pos < max_pos:
                scrollbar.setValue(current_pos + self.scroll_speed)
                
    def scroll_up(self):
        scrollbar = self.script_display.verticalScrollBar()
        current_pos = scrollbar.value()
        scrollbar.setValue(current_pos - 20)
        
    def scroll_down(self):
        scrollbar = self.script_display.verticalScrollBar()
        current_pos = scrollbar.value()
        scrollbar.setValue(current_pos + 20)
        
    def reset_to_top(self):
        scrollbar = self.script_display.verticalScrollBar()
        scrollbar.setValue(0)
        
    def scroll_to_bottom(self):
        scrollbar = self.script_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def add_script_text(self, text):
        """Thêm text vào script (có thể dùng để cập nhật script động)"""
        current_text = self.script_display.toPlainText()
        if current_text:
            current_text += "\n\n" + text
        else:
            current_text = text
            
        self.script_display.setPlainText(current_text)
        
    def clear_script(self):
        """Xóa toàn bộ script"""
        self.script_display.clear()
        self.script_file = None
        self.setWindowTitle("Script Nói")
        
    def save_script(self):
        """Lưu script hiện tại"""
        if not self.script_file:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Lưu script", "", 
                "Text Files (*.txt);;All Files (*)"
            )
            if file_path:
                self.script_file = file_path
            else:
                return
                
        try:
            content = self.script_display.toPlainText()
            with open(self.script_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            QMessageBox.information(self, "Thành công", "Đã lưu script!")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu file: {str(e)}")
            
    def closeEvent(self, event):
        """Xử lý khi đóng cửa sổ"""
        self.scroll_timer.stop()
        event.accept() 