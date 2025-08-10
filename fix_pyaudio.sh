#!/bin/bash

echo "🔧 Sửa lỗi cài đặt pyaudio..."
echo ""

# Cài đặt portaudio và dependencies cần thiết
echo "📦 Cài đặt portaudio và dependencies cần thiết..."
sudo apt update
sudo apt install -y portaudio19-dev python3-dev build-essential

if [ $? -eq 0 ]; then
    echo "✅ portaudio và dependencies đã được cài đặt thành công"
else
    echo "❌ Không thể cài đặt portaudio"
    echo "Bạn có thể cài đặt thủ công: sudo apt install portaudio19-dev python3-dev build-essential"
    exit 1
fi

# Gỡ cài đặt pyaudio cũ (nếu có)
echo "🗑️  Gỡ cài đặt pyaudio cũ..."
pip3 uninstall -y pyaudio

# Cài đặt pyaudio mới
echo "📦 Cài đặt pyaudio..."
pip3 install pyaudio

if [ $? -eq 0 ]; then
    echo "✅ pyaudio đã được cài đặt thành công!"
    echo ""
    echo "🔍 Kiểm tra cài đặt..."
    python3 -c "import pyaudio; print('✅ pyaudio hoạt động bình thường')"
else
    echo "❌ Không thể cài đặt pyaudio"
    echo "Thử cài đặt từ source:"
    pip3 install --no-binary :all: pyaudio
    
    if [ $? -eq 0 ]; then
        echo "✅ pyaudio đã được cài đặt thành công từ source!"
    else
        echo "❌ Vẫn không thể cài đặt pyaudio"
        echo "Vui lòng kiểm tra lỗi và thử lại"
        exit 1
    fi
fi

echo ""
echo "🎉 Đã sửa lỗi pyaudio thành công!"
echo "Bây giờ bạn có thể chạy lại script cài đặt chính: ./install.sh" 