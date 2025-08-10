# Ứng dụng Trình chiếu Gọn nhẹ cho Linux

Một ứng dụng trình chiếu đơn giản, gọn nhẹ được viết bằng Python và PyQt6, hỗ trợ hiển thị PDF và PowerPoint với các tính năng bổ sung.

## Tính năng chính

### 🎯 Trình chiếu tài liệu
- **Hỗ trợ định dạng**: PDF (.pdf), PowerPoint (.pptx, .ppt)
- **Điều hướng**: Chuyển slide bằng nút bấm, thanh trượt hoặc phím tắt
- **Chế độ toàn màn hình**: F11 để bật/tắt toàn màn hình
- **Hiển thị thông tin**: Số slide hiện tại và tổng số slide

### 📝 Cửa sổ Script nói
- **Hiển thị riêng biệt**: Cửa sổ script luôn ở trên cùng
- **Tùy chỉnh**: Thay đổi font, màu sắc, kích thước
- **Tự động cuộn**: Cuộn script tự động với tốc độ có thể điều chỉnh
- **Phím tắt**: Mũi tên lên/xuống, Home/End để điều hướng

### ✏️ Vẽ trực tiếp
- **Vẽ tự do**: Vẽ trực tiếp lên màn hình trình chiếu
- **Tùy chỉnh**: Thay đổi màu sắc và độ dày nét vẽ
- **Công cụ**: Xóa, hoàn tác, lưu nét vẽ
- **Phím tắt**: Delete để xóa, Ctrl+Z để hoàn tác, Escape để ẩn

### 🎥 Ghi màn hình
- **Ghi màn hình trình chiếu**: Chỉ ghi khu vực trình chiếu, không ghi cửa sổ script
- **Chất lượng cao**: Hỗ trợ FPS và chất lượng video có thể điều chỉnh
- **Định dạng MP4**: Xuất file video MP4 với codec H.264
- **Quản lý file**: Tự động tạo thư mục và đặt tên file theo thời gian

## Phím tắt

| Phím | Chức năng |
|------|-----------|
| **←/→** | Chuyển slide trước/sau |
| **F11** | Bật/tắt toàn màn hình |
| **D** | Bật/tắt chế độ vẽ |
| **Delete** | Xóa toàn bộ nét vẽ |
| **Ctrl+Z** | Hoàn tác nét vẽ cuối |
| **Escape** | Ẩn overlay vẽ |
| **↑/↓** | Cuộn script lên/xuống |
| **Home/End** | Về đầu/cuối script |

## Cài đặt

### Yêu cầu hệ thống
- Linux (đã test trên Ubuntu 20.04+)
- Python 3.8+
- ffmpeg (để ghi màn hình)

### Cài đặt dependencies

```bash
# Cài đặt ffmpeg
sudo apt update
sudo apt install ffmpeg

# Cài đặt Python dependencies
pip install -r requirements.txt
```

### Chạy ứng dụng

```bash
python3 main.py
```

## Cấu trúc dự án

```
draft-presentation/
├── main.py                 # Giao diện chính
├── presentation_viewer.py  # Xử lý PDF/PPTX
├── script_window.py        # Cửa sổ script
├── drawing_overlay.py      # Overlay vẽ
├── screen_recorder.py      # Ghi màn hình
├── requirements.txt        # Dependencies
└── README.md              # Hướng dẫn
```

## Sử dụng

### 1. Mở file trình chiếu
- Click nút "Mở File" hoặc sử dụng menu
- Chọn file PDF hoặc PowerPoint
- File sẽ được tải và hiển thị slide đầu tiên

### 2. Điều khiển trình chiếu
- Sử dụng nút "Trước"/"Sau" hoặc phím mũi tên
- Kéo thanh trượt để chuyển nhanh đến slide cụ thể
- F11 để bật chế độ toàn màn hình

### 3. Mở cửa sổ Script
- Click nút "Mở Script"
- Cửa sổ script sẽ xuất hiện ở bên phải
- Mở file .txt chứa nội dung script
- Tùy chỉnh font, màu sắc theo ý muốn

### 4. Bật chế độ vẽ
- Click nút "Bật Vẽ" hoặc nhấn phím D
- Overlay vẽ sẽ xuất hiện
- Vẽ tự do bằng chuột
- Sử dụng thanh công cụ để thay đổi màu, độ dày

### 5. Ghi màn hình
- Click nút "Ghi Màn hình"
- Chỉ ghi khu vực trình chiếu (không ghi cửa sổ script)
- Click "Dừng Ghi" để dừng
- File video sẽ được lưu trong thư mục `recordings/`

## Tùy chỉnh

### Thay đổi FPS ghi màn hình
Chỉnh sửa file `screen_recorder.py`:
```python
self.fps = 30  # Thay đổi giá trị này
```

### Thay đổi chất lượng video
Chỉnh sửa file `screen_recorder.py`:
```python
'-crf', str(23),  # Giá trị từ 18-28, càng thấp càng chất lượng cao
```

### Thay đổi độ phân giải ghi
Chỉnh sửa file `screen_recorder.py`:
```python
'-s', '1920x1080',  # Thay đổi độ phân giải
```

## Xử lý sự cố

### Lỗi "ffmpeg not found"
```bash
sudo apt install ffmpeg
```

### Lỗi "No module named 'PyQt6'"
```bash
pip install PyQt6
```

### Lỗi "No module named 'fitz'"
```bash
pip install PyMuPDF
```

### Lỗi "No module named 'cv2'"
```bash
pip install opencv-python
```

## Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request để cải thiện ứng dụng.

