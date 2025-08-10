#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor

class ScreenRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ghi màn hình")
        self.setGeometry(100, 100, 400, 200)
        
        # Biến ghi màn hình
        self.is_recording = False
        self.recording_thread = None
        self.output_file = None
        self.fps = 30
        self.quality = 80
        
        # Thiết lập giao diện
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Thông tin trạng thái
        self.status_label = QLabel("Sẵn sàng ghi màn hình")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #e9ecef;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Nút điều khiển
        control_layout = QHBoxLayout()
        
        self.record_btn = QPushButton("Bắt đầu ghi")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.record_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        self.stop_btn = QPushButton("Dừng ghi")
        self.stop_btn.clicked.connect(self.stop_recording)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        
        control_layout.addWidget(self.record_btn)
        control_layout.addWidget(self.stop_btn)
        layout.addLayout(control_layout)
        
        # Nút thiết lập
        settings_layout = QHBoxLayout()
        
        self.settings_btn = QPushButton("Thiết lập")
        self.settings_btn.clicked.connect(self.show_settings)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        self.open_folder_btn = QPushButton("Mở thư mục")
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        self.open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        
        settings_layout.addWidget(self.settings_btn)
        settings_layout.addWidget(self.open_folder_btn)
        layout.addLayout(settings_layout)
        
        # Thông tin ghi
        self.info_label = QLabel("Chưa có file ghi nào")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #6c757d;
                padding: 5px;
            }
        """)
        layout.addWidget(self.info_label)
        
    def toggle_recording(self):
        """Bật/tắt ghi màn hình"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Bắt đầu ghi màn hình"""
        try:
            # Tạo tên file output
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file = f"presentation_recording_{timestamp}.mp4"
            
            # Tạo thư mục output nếu chưa có
            output_dir = "recordings"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            self.output_file = os.path.join(output_dir, self.output_file)
            
            # Bắt đầu thread ghi màn hình
            self.recording_thread = RecordingThread(self.output_file, self.fps, self.quality)
            self.recording_thread.recording_started.connect(self.on_recording_started)
            self.recording_thread.recording_stopped.connect(self.on_recording_stopped)
            self.recording_thread.error_occurred.connect(self.on_recording_error)
            
            self.recording_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể bắt đầu ghi: {str(e)}")
            
    def stop_recording(self):
        """Dừng ghi màn hình"""
        if self.recording_thread and self.recording_thread.isRunning():
            self.recording_thread.stop_recording()
            
    def on_recording_started(self):
        """Xử lý khi bắt đầu ghi"""
        self.is_recording = True
        self.record_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Đang ghi màn hình...")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #d4edda;
                color: #155724;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        
    def on_recording_stopped(self):
        """Xử lý khi dừng ghi"""
        self.is_recording = False
        self.record_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Đã dừng ghi màn hình")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #fff3cd;
                color: #856404;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        
        if self.output_file and os.path.exists(self.output_file):
            file_size = os.path.getsize(self.output_file) / (1024 * 1024)  # MB
            self.info_label.setText(f"File: {os.path.basename(self.output_file)} ({file_size:.1f} MB)")
            
    def on_recording_error(self, error_msg):
        """Xử lý khi có lỗi ghi"""
        QMessageBox.critical(self, "Lỗi ghi màn hình", error_msg)
        self.on_recording_stopped()
        
    def show_settings(self):
        """Hiển thị cửa sổ thiết lập"""
        # Có thể mở rộng để thêm các tùy chọn khác
        QMessageBox.information(self, "Thiết lập", 
                              f"FPS: {self.fps}\nChất lượng: {self.quality}%\n"
                              "Để thay đổi, hãy chỉnh sửa trực tiếp trong code.")
        
    def open_output_folder(self):
        """Mở thư mục chứa file ghi"""
        output_dir = "recordings"
        if os.path.exists(output_dir):
            import subprocess
            try:
                subprocess.run(["xdg-open", output_dir])  # Linux
            except:
                try:
                    subprocess.run(["open", output_dir])  # macOS
                except:
                    subprocess.run(["explorer", output_dir])  # Windows
        else:
            QMessageBox.information(self, "Thông tin", "Chưa có thư mục recordings nào.")
            
    def is_recording(self):
        """Kiểm tra trạng thái ghi"""
        return self.is_recording
        
    def closeEvent(self, event):
        """Xử lý khi đóng cửa sổ"""
        if self.is_recording:
            self.stop_recording()
        event.accept()


class RecordingThread(QThread):
    """Thread riêng biệt để ghi màn hình"""
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, output_file, fps=30, quality=80):
        super().__init__()
        self.output_file = output_file
        self.fps = fps
        self.quality = quality
        self.is_recording = False
        
    def run(self):
        """Chạy thread ghi màn hình"""
        try:
            self.is_recording = True
            self.recording_started.emit()
            
            # Sử dụng ffmpeg để ghi màn hình (cần cài đặt ffmpeg)
            self._record_with_ffmpeg()
            
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.is_recording = False
            self.recording_stopped.emit()
            
    def _record_with_ffmpeg(self):
        """Ghi màn hình sử dụng ffmpeg"""
        try:
            import subprocess
            
            # Lệnh ffmpeg để ghi màn hình
            cmd = [
                'ffmpeg',
                '-f', 'x11grab',  # Linux X11
                '-s', '1920x1080',  # Độ phân giải
                '-i', ':0.0',  # Display
                '-f', 'alsa',  # Audio
                '-i', 'default',  # Audio device
                '-c:v', 'libx264',  # Video codec
                '-preset', 'ultrafast',  # Preset
                '-crf', str(23),  # Chất lượng video
                '-c:a', 'aac',  # Audio codec
                '-b:a', '128k',  # Audio bitrate
                '-y',  # Ghi đè file
                self.output_file
            ]
            
            # Chạy ffmpeg
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Chờ cho đến khi dừng
            while self.is_recording:
                if process.poll() is not None:
                    break
                self.msleep(100)  # Sleep 100ms
                
            # Dừng process
            if process.poll() is None:
                process.terminate()
                process.wait()
                
        except FileNotFoundError:
            # Nếu không có ffmpeg, sử dụng phương pháp thay thế
            self._record_with_python()
            
    def _record_with_python(self):
        """Ghi màn hình sử dụng Python (fallback)"""
        try:
            # Sử dụng mss để chụp màn hình
            import mss
            
            with mss.mss() as sct:
                # Chụp màn hình chính
                monitor = sct.monitors[1]  # Màn hình chính
                
                # Tạo video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(self.output_file, fourcc, self.fps, 
                                    (monitor['width'], monitor['height']))
                
                frame_count = 0
                max_frames = self.fps * 60  # Ghi tối đa 1 phút
                
                while self.is_recording and frame_count < max_frames:
                    # Chụp màn hình
                    screenshot = sct.grab(monitor)
                    
                    # Chuyển đổi sang numpy array
                    frame = np.array(screenshot)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    
                    # Ghi frame
                    out.write(frame)
                    
                    frame_count += 1
                    self.msleep(1000 // self.fps)  # Sleep theo FPS
                    
                out.release()
                
        except ImportError:
            self.error_occurred.emit("Cần cài đặt ffmpeg hoặc mss để ghi màn hình")
            
    def stop_recording(self):
        """Dừng ghi màn hình"""
        self.is_recording = False 