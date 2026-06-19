import tkinter as tk
from tkinter import messagebox

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f4f6f9")
        
        # Tiêu đề
        title = tk.Label(self, text="ĐĂNG NHẬP HỆ THỐNG THI TRẮC NGHIỆM", font=("Helvetica", 16, "bold"), bg="#f4f6f9", fg="#1a73e8")
        title.pack(pady=50)
        
        # Khung chứa Form đăng nhập
        self.form = tk.Frame(self, bg="white", bd=1, relief="solid", padx=40, pady=35)
        self.form.pack(pady=10)
        
        # Ô nhập Username
        tk.Label(self.form, text="Tên tài khoản (Username):", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w", pady=5)
        self.username_entry = tk.Entry(self.form, font=("Helvetica", 11), width=30)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "Nhập tên của bạn ở đây...") # Placeholder text
        
        # Lắng nghe sự kiện gõ chữ trên ô Username để tự động ẩn/hiện ô Password
        self.username_entry.bind("<KeyRelease>", self.toggle_password_field)
        
        # Khởi tạo trước các widget của Password nhưng chưa cho hiển thị (pack)
        self.lbl_pass = tk.Label(self.form, text="Mật khẩu bảo mật Admin:", font=("Helvetica", 10, "bold"), bg="white", fg="#d32f2f")
        self.password_entry = tk.Entry(self.form, font=("Helvetica", 11), width=30, show="*")
        
        # Chú thích hướng dẫn quyền
        self.hint = tk.Label(self.form, text=" Nhập tài khoản 'admin' để kích hoạt tài khoản Giáo Viên", font=("Helvetica", 9, "italic"), bg="white", fg="#5f6368")
        self.hint.pack(pady=12)
        
        # Nút bấm đăng nhập
        btn_login = tk.Button(self.form, text="ĐĂNG NHẬP", font=("Helvetica", 11, "bold"), bg="#1a73e8", fg="white", width=25, pady=6, command=self.handle_login, relief="flat", cursor="hand2")
        btn_login.pack(pady=10)

    def toggle_password_field(self, event=None):
        """Hàm tự động ẩn/hiện ô nhập mật khẩu dựa vào tên Username"""
        username = self.username_entry.get().strip().lower()
        
        if username == "admin":
            # Nếu gõ đúng chữ admin, ẩn dòng gợi ý và chèn ô Password vào giữa
            self.hint.pack_forget()
            self.lbl_pass.pack(anchor="w", pady=5)
            self.password_entry.pack(pady=5)
            self.hint.pack(pady=12) # Đẩy dòng gợi ý xuống dưới cùng lại
        else:
            # Nếu gõ tên khác, ẩn hoàn toàn ô nhập mật khẩu đi
            self.lbl_pass.pack_forget()
            self.password_entry.pack_forget()

    def handle_login(self):
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showwarning("Thông báo", "Vui lòng nhập tên tài khoản (Username)!")
            return
            
        # PHÂN QUYỀN ĐĂNG NHẬP
        if username.lower() == "admin":
            password = self.password_entry.get().strip()
            # Kiểm tra mật khẩu mặc định của admin
            if password == "123456":
                self.controller.current_user = "Giáo Viên Quản Trị"
                self.controller.current_role = "Admin"
                messagebox.showinfo("Thành công", "Đăng nhập quyền Giáo viên thành công!")
                self.controller.show_admin_frame()
            else:
                messagebox.showerror("Sai mật khẩu", "Mật khẩu Admin không chính xác!")
        else:
            # Học sinh vào thẳng mà không cần mật khẩu
            self.controller.current_user = username
            self.controller.current_role = "User"
            messagebox.showinfo("Thành công", f"Chào mừng học sinh {username} đăng nhập thành công!")
            self.controller.show_user_frame()