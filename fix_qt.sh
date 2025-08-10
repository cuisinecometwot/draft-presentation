#!/bin/bash

echo "🔧 Sửa lỗi Qt platform plugin..."
echo ""

# Cài đặt các thư viện X11 cần thiết
echo "📦 Cài đặt thư viện X11..."
sudo apt update
sudo apt install -y libxcb-cursor0 libxcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 libx11-xcb1 libxcb-dri2-0 libxcb-dri3-0 libxcb-glx0 libxcb-present0

if [ $? -eq 0 ]; then
    echo "✅ Thư viện X11 đã được cài đặt thành công"
else
    echo "❌ Không thể cài đặt thư viện X11"
    exit 1
fi

# Cài đặt Qt6 libraries
echo ""
echo "📦 Cài đặt Qt6 libraries..."
sudo apt install -y qt6-base-dev qt6-base-dev-tools libqt6gui6 libqt6widgets6 libqt6core6 qt6-qpa-plugins qt6-gtk-platformtheme

if [ $? -eq 0 ]; then
    echo "✅ Qt6 libraries đã được cài đặt thành công"
else
    echo "❌ Không thể cài đặt Qt6 libraries"
    exit 1
fi

# Cài đặt thêm các thư viện X11 khác
echo ""
echo "📦 Cài đặt thêm thư viện X11..."
sudo apt install -y libx11-6 libxext6 libxrender1 libxss1 libxtst6 libxi6

if [ $? -eq 0 ]; then
    echo "✅ Thêm thư viện X11 đã được cài đặt thành công"
else
    echo "❌ Không thể cài đặt thêm thư viện X11"
fi

echo ""
echo "🎉 Đã sửa lỗi Qt platform plugin thành công!"
echo "Bây giờ bạn có thể chạy ứng dụng: python3 main.py"
echo ""
echo "🔍 Kiểm tra cài đặt..."
python3 -c "from PyQt6.QtWidgets import QApplication; print('✅ PyQt6 hoạt động bình thường')"

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Thử chạy ứng dụng..."
    echo "Nhấn Ctrl+C để dừng nếu cần"
    python3 main.py
else
    echo "❌ Vẫn có vấn đề với PyQt6"
    echo "Vui lòng kiểm tra lại cài đặt"
fi 