import tkinter as tk
import json
import os
from core import datahand

class QuizApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HỆ THỐNG KIỂM TRA TRẮC NGHIỆM TRỰC TUYẾN")
        self.geometry("950x680")
        self.minsize(900, 620)
        
        self.current_user = None
        self.current_role = None
        
        # ĐẢM BẢO FILE KẾT QUẢ ĐƯỢC KHỞI TẠO ĐÚNG ĐỊNH DẠNG MẢNG
        if not os.path.exists(datahand.RESULTS_FILE) or os.path.getsize(datahand.RESULTS_FILE) == 0:
            with open(datahand.RESULTS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

        # Nạp dữ liệu toàn cục thông qua module datahand sẵn có của bạn
        self.bank = datahand.loadData(datahand.QUESTIONS_FILE)
        self.results_db = datahand.loadData(datahand.RESULTS_FILE)
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.current_frame = None
        self.show_login_frame()

    def refresh_results_from_disk(self):
        """Đọc lại file kết quả từ ổ đĩa để cập nhật dữ liệu mới nhất"""
        self.results_db = datahand.loadData(datahand.RESULTS_FILE)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self.container, self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    def show_login_frame(self):
        self.current_user = None
        self.current_role = None
        from gui.login_frame import LoginFrame
        self.switch_frame(LoginFrame)

    def show_admin_frame(self):
        from gui.admin_frame import AdminFrame
        self.switch_frame(AdminFrame)

    def show_user_frame(self):
        from gui.user_frame import UserFrame
        self.switch_frame(UserFrame)

if __name__ == "__main__":
    app = QuizApplication()
    app.mainloop()