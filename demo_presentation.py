#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo script để test ứng dụng trình chiếu
Chạy script này để kiểm tra các tính năng cơ bản
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt

def create_demo_pdf():
    """Tạo file PDF demo đơn giản"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        filename = "demo_presentation.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Trang 1: Tiêu đề
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height-100, "Demo Trình chiếu")
        
        c.setFont("Helvetica", 16)
        c.drawCentredString(width/2, height-150, "Ứng dụng trình chiếu gọn nhẹ cho Linux")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, height-200, "Tính năng:")
        c.drawString(120, height-220, "• Hỗ trợ PDF và PowerPoint")
        c.drawString(120, height-240, "• Cửa sổ script riêng biệt")
        c.drawString(120, height-260, "• Vẽ trực tiếp lên màn hình")
        c.drawString(120, height-280, "• Ghi màn hình trình chiếu")
        
        c.showPage()
        
        # Trang 2: Tính năng chi tiết
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height-100, "Tính năng chi tiết")
        
        c.setFont("Helvetica", 12)
        y_pos = height-150
        
        features = [
            "🎯 Trình chiếu tài liệu",
            "   - Hỗ trợ PDF và PowerPoint",
            "   - Điều hướng dễ dàng",
            "   - Chế độ toàn màn hình",
            "",
            "📝 Cửa sổ Script",
            "   - Hiển thị riêng biệt",
            "   - Tùy chỉnh font và màu",
            "   - Tự động cuộn",
            "",
            "✏️ Vẽ trực tiếp",
            "   - Vẽ tự do lên màn hình",
            "   - Thay đổi màu và độ dày",
            "   - Công cụ xóa và hoàn tác",
            "",
            "🎥 Ghi màn hình",
            "   - Chỉ ghi khu vực trình chiếu",
            "   - Xuất file MP4 chất lượng cao",
            "   - Quản lý file tự động"
        ]
        
        for feature in features:
            c.drawString(100, y_pos, feature)
            y_pos -= 20
            
        c.showPage()
        
        # Trang 3: Hướng dẫn sử dụng
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height-100, "Hướng dẫn sử dụng")
        
        c.setFont("Helvetica", 12)
        y_pos = height-150
        
        instructions = [
            "1. Mở file trình chiếu (PDF/PPTX)",
            "2. Sử dụng phím mũi tên để chuyển slide",
            "3. F11 để bật chế độ toàn màn hình",
            "4. Nhấn D để bật chế độ vẽ",
            "5. Mở cửa sổ script để hiển thị nội dung",
            "6. Sử dụng nút ghi màn hình để record",
            "",
            "Phím tắt:",
            "• ←/→: Chuyển slide",
            "• F11: Toàn màn hình",
            "• D: Bật/tắt vẽ",
            "• Delete: Xóa nét vẽ",
            "• Ctrl+Z: Hoàn tác",
            "• Escape: Ẩn overlay vẽ"
        ]
        
        for instruction in instructions:
            c.drawString(100, y_pos, instruction)
            y_pos -= 20
            
        c.save()
        print(f"✅ Đã tạo file demo: {filename}")
        return filename
        
    except ImportError:
        print("⚠️  Không thể tạo PDF demo (cần cài đặt reportlab)")
        return None

def create_demo_script():
    """Tạo file script demo"""
    filename = "demo_script.txt"
    
    script_content = """=== SCRIPT TRÌNH CHIẾU DEMO ===

Chào mừng đến với buổi trình chiếu demo!

1. GIỚI THIỆU (30 giây)
   Chào mừng quý vị đến với buổi trình chiếu về ứng dụng trình chiếu gọn nhẹ cho Linux.
   
   Ứng dụng này được thiết kế đặc biệt cho người dùng Linux, với giao diện đơn giản
   và các tính năng hữu ích cho việc trình chiếu chuyên nghiệp.

2. TÍNH NĂNG CHÍNH (2 phút)
   
   a) Trình chiếu tài liệu:
   - Hỗ trợ đầy đủ định dạng PDF và PowerPoint
   - Điều hướng slide dễ dàng với phím tắt
   - Chế độ toàn màn hình chuyên nghiệp
   
   b) Cửa sổ Script nói:
   - Hiển thị riêng biệt, luôn ở trên cùng
   - Tùy chỉnh font, màu sắc theo ý muốn
   - Tự động cuộn với tốc độ có thể điều chỉnh
   
   c) Vẽ trực tiếp:
   - Vẽ tự do lên màn hình trình chiếu
   - Thay đổi màu sắc và độ dày nét vẽ
   - Công cụ xóa và hoàn tác thông minh
   
   d) Ghi màn hình:
   - Chỉ ghi khu vực trình chiếu, không ghi script
   - Xuất file MP4 chất lượng cao
   - Quản lý file tự động theo thời gian

3. LỢI ÍCH (1 phút)
   
   - Gọn nhẹ, không chiếm nhiều tài nguyên
   - Giao diện đơn giản, dễ sử dụng
   - Tích hợp nhiều tính năng trong một ứng dụng
   - Tương thích tốt với hệ thống Linux
   - Mã nguồn mở, có thể tùy chỉnh

4. KẾT LUẬN (30 giây)
   
   Ứng dụng trình chiếu này là giải pháp hoàn hảo cho người dùng Linux
   cần một công cụ trình chiếu đơn giản nhưng đầy đủ tính năng.
   
   Với giao diện thân thiện và các tính năng hữu ích, ứng dụng sẽ giúp
   buổi trình chiếu của bạn trở nên chuyên nghiệp và hiệu quả hơn.

=== LƯU Ý KHI SỬ DỤNG ===
- Đảm bảo đã cài đặt ffmpeg để ghi màn hình
- Sử dụng phím tắt để thao tác nhanh
- Tùy chỉnh font và màu script cho dễ đọc
- Luyện tập trước khi trình chiếu thực tế

=== CẢM ƠN ===
Cảm ơn quý vị đã quan tâm đến ứng dụng trình chiếu này!
"""
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"✅ Đã tạo file script demo: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Lỗi khi tạo script demo: {e}")
        return None

def test_basic_functionality():
    """Test các tính năng cơ bản"""
    print("🔍 Kiểm tra các tính năng cơ bản...")
    
    # Test PyQt6
    try:
        app = QApplication(sys.argv)
        print("✅ PyQt6 hoạt động bình thường")
    except Exception as e:
        print(f"❌ Lỗi PyQt6: {e}")
        return False
    
    # Test các module khác
    modules_to_test = [
        ('fitz', 'PyMuPDF'),
        ('pptx', 'python-pptx'),
        ('PIL', 'Pillow'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy')
    ]
    
    for module_name, package_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {package_name} hoạt động bình thường")
        except ImportError:
            print(f"❌ {package_name} chưa được cài đặt")
    
    return True

def main():
    """Hàm chính"""
    print("🚀 Demo Ứng dụng Trình chiếu Linux")
    print("=" * 50)
    
    # Test chức năng cơ bản
    if not test_basic_functionality():
        print("\n❌ Không thể khởi tạo ứng dụng")
        return
    
    # Tạo file demo
    print("\n📝 Tạo file demo...")
    pdf_file = create_demo_pdf()
    script_file = create_demo_script()
    
    print("\n📋 Tóm tắt:")
    if pdf_file:
        print(f"   • File trình chiếu: {pdf_file}")
    if script_file:
        print(f"   • File script: {script_file}")
    
    print("\n🎯 Để chạy ứng dụng:")
    print("   python3 main.py")
    print("\n📚 Để xem hướng dẫn chi tiết:")
    print("   cat README.md")
    
    print("\n✨ Demo hoàn tất! Bạn có thể chạy ứng dụng chính.")

if __name__ == "__main__":
    main() 