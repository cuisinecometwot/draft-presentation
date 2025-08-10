#!/bin/bash

# Script cài đặt ứng dụng trình chiếu
# Tác giả: AI Assistant
# Phiên bản: 1.0

echo "=========================================="
echo "  Cài đặt Ứng dụng Trình chiếu Linux"
echo "=========================================="
echo ""

# Kiểm tra hệ điều hành
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Script này chỉ hỗ trợ Linux"
    exit 1
fi

# Kiểm tra Python
echo "🔍 Kiểm tra Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được cài đặt"
    echo "Vui lòng cài đặt Python3 trước:"
    echo "sudo apt update && sudo apt install python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION đã được cài đặt"

# Kiểm tra pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 không được cài đặt"
    echo "Vui lòng cài đặt pip3:"
    echo "sudo apt install python3-pip"
    exit 1
fi

echo "✅ pip3 đã được cài đặt"

# Cài đặt ffmpeg
echo ""
echo "🔍 Kiểm tra ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Cài đặt ffmpeg..."
    sudo apt update
    sudo apt install -y ffmpeg
    if [ $? -eq 0 ]; then
        echo "✅ ffmpeg đã được cài đặt thành công"
    else
        echo "❌ Không thể cài đặt ffmpeg"
        echo "Bạn có thể cài đặt thủ công: sudo apt install ffmpeg"
    fi
else
    echo "✅ ffmpeg đã được cài đặt"
fi

# Cài đặt portaudio và các dependencies cần thiết
echo ""
echo "📦 Cài đặt portaudio và dependencies cần thiết..."
sudo apt update
sudo apt install -y portaudio19-dev python3-dev build-essential

if [ $? -eq 0 ]; then
    echo "✅ portaudio và dependencies đã được cài đặt thành công"
else
    echo "❌ Không thể cài đặt portaudio"
    echo "Bạn có thể cài đặt thủ công: sudo apt install portaudio19-dev python3-dev build-essential"
fi

# Cài đặt các thư viện X11 và Qt cần thiết
echo ""
echo "📦 Cài đặt thư viện X11 và Qt..."
sudo apt install -y libxcb-cursor0 libxcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 libx11-xcb1 libxcb-dri2-0 libxcb-dri3-0 libxcb-glx0 libxcb-present0

if [ $? -eq 0 ]; then
    echo "✅ Thư viện X11 đã được cài đặt thành công"
else
    echo "❌ Không thể cài đặt thư viện X11"
fi

# Cài đặt Qt6 libraries
echo ""
echo "📦 Cài đặt Qt6 libraries..."
sudo apt install -y qt6-base-dev qt6-base-dev-tools libqt6gui6 libqt6widgets6 libqt6core6 qt6-qpa-plugins qt6-gtk-platformtheme

if [ $? -eq 0 ]; then
    echo "✅ Qt6 libraries đã được cài đặt thành công"
else
    echo "❌ Không thể cài đặt Qt6 libraries"
fi

# Cài đặt Python dependencies
echo ""
echo "📦 Cài đặt Python dependencies..."
if [ -f "requirements.txt" ]; then
    echo "Cài đặt từ requirements.txt..."
    
    # Cài đặt pyaudio trước (cần portaudio)
    echo "📦 Cài đặt pyaudio..."
    pip3 install pyaudio
    
    if [ $? -eq 0 ]; then
        echo "✅ pyaudio đã được cài đặt thành công"
    else
        echo "❌ Không thể cài đặt pyaudio"
        echo "Thử cài đặt từ source:"
        pip3 install --no-binary :all: pyaudio
    fi
    
    # Cài đặt các dependencies khác
    echo "📦 Cài đặt các dependencies khác..."
    pip3 install PyQt6 PyMuPDF python-pptx Pillow opencv-python numpy keyboard
    
    if [ $? -eq 0 ]; then
        echo "✅ Tất cả dependencies đã được cài đặt thành công"
    else
        echo "❌ Có lỗi khi cài đặt dependencies"
        echo "Thử cài đặt từng package một:"
        pip3 install PyQt6 PyMuPDF python-pptx Pillow opencv-python numpy keyboard
    fi
else
    echo "❌ Không tìm thấy requirements.txt"
    echo "Cài đặt dependencies thủ công:"
    
    # Cài đặt pyaudio trước
    echo "📦 Cài đặt pyaudio..."
    pip3 install pyaudio
    
    # Cài đặt các dependencies khác
    pip3 install PyQt6 PyMuPDF python-pptx Pillow opencv-python numpy keyboard
fi

# Tạo thư mục recordings
echo ""
echo "📁 Tạo thư mục recordings..."
mkdir -p recordings
echo "✅ Thư mục recordings đã được tạo"

# Tạo file script mẫu
echo ""
echo "📝 Tạo file script mẫu..."
cat > sample_script.txt << 'EOF'
=== SCRIPT TRÌNH CHIẾU MẪU ===

Chào mừng đến với buổi trình chiếu!

1. Giới thiệu
   - Tên dự án
   - Mục tiêu
   - Phạm vi

2. Nội dung chính
   - Tính năng 1
   - Tính năng 2
   - Tính năng 3

3. Kết luận
   - Tóm tắt
   - Hướng phát triển
   - Cảm ơn

=== HƯỚNG DẪN SỬ DỤNG ===
- Sử dụng phím mũi tên để cuộn
- Home/End để về đầu/cuối
- Tùy chỉnh font và màu sắc
EOF

echo "✅ File script mẫu đã được tạo: sample_script.txt"

# Tạo desktop shortcut
echo ""
echo "🖥️  Tạo desktop shortcut..."
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    cat > "$DESKTOP_DIR/Presentation App.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Ứng dụng Trình chiếu
Comment=Trình chiếu PDF và PowerPoint với tính năng bổ sung
Exec=$(pwd)/main.py
Icon=application-x-ms-powerpoint
Terminal=false
Categories=Office;Presentation;
EOF

    chmod +x "$DESKTOP_DIR/Presentation App.desktop"
    echo "✅ Desktop shortcut đã được tạo"
else
    echo "⚠️  Không tìm thấy thư mục Desktop"
fi

# Tạo script chạy
echo ""
echo "🚀 Tạo script chạy..."
cat > run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 main.py
EOF

chmod +x run.sh
echo "✅ Script chạy đã được tạo: run.sh"

# Kiểm tra cài đặt
echo ""
echo "🔍 Kiểm tra cài đặt..."
echo "Kiểm tra các module Python..."

# Tạo file Python tạm để kiểm tra
cat > check_modules.py << 'EOF'
import sys
modules = ['PyQt6', 'fitz', 'pptx', 'PIL', 'cv2', 'numpy', 'pyaudio']
missing = []

for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError:
        print(f'❌ {module}')
        missing.append(module)

if missing:
    print(f'\n❌ Thiếu {len(missing)} module: {", ".join(missing)}')
    print('Vui lòng cài đặt lại: pip3 install -r requirements.txt')
    sys.exit(1)
else:
    print('\n🎉 Tất cả module đã được cài đặt thành công!')
EOF

python3 check_modules.py
RESULT=$?

# Xóa file tạm
rm -f check_modules.py

if [ $RESULT -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  🎉 Cài đặt hoàn tất thành công!"
    echo "=========================================="
    echo ""
    echo "📱 Cách sử dụng:"
    echo "  1. Chạy ứng dụng: ./run.sh"
    echo "  2. Hoặc: python3 main.py"
    echo "  3. Hoặc click vào desktop shortcut"
    echo ""
    echo "📚 Tài liệu: README.md"
    echo "📁 Thư mục recordings: ./recordings/"
    echo "📝 Script mẫu: sample_script.txt"
    echo ""
    echo "🚀 Chạy ứng dụng ngay bây giờ? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Khởi động ứng dụng..."
        python3 main.py
    fi
else
    echo ""
    echo "❌ Cài đặt không hoàn tất"
    echo "Vui lòng kiểm tra lỗi và thử lại"
    exit 1
fi 