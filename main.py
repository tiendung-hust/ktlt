from gui.app import QuizApplication

def main():
    """Hàm khởi chạy toàn bộ hệ thống quản lý và thi trắc nghiệm"""
    # Khởi tạo đối tượng ứng dụng từ Controller chính (app.py)
    app = QuizApplication()
    
    # Kích hoạt vòng lặp vô hạn để giữ giao diện đồ họa Tkinter luôn hiển thị
    app.mainloop()

if __name__ == "__main__":
    main()