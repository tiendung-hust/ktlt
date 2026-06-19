import tkinter as tk
from tkinter import ttk, messagebox
import time
from core.algorithms import bubble_sort 
from core.exam import exam, results      
from core import datahand

class UserFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.active_exam_data = None
        self.radio_variables = []
        self.exam_timer_running = False
        
        self.render_start_frame()

    def clean_screen(self):
        for widget in self.winfo_children(): widget.destroy()
    def render_start_frame(self):
        self.clean_screen()
        self.exam_timer_running = False
        
        bar = tk.Frame(self, bg="#1a73e8", pady=8)
        bar.pack(fill="x")
        tk.Label(bar, text=f"Tài khoản thí sinh: {self.controller.current_user}", fg="white", bg="#1a73e8", font=("Helvetica", 10, "bold")).pack(side="left", padx=15)
        tk.Button(bar, text="Đăng xuất", bg="#d32f2f", fg="white", font=("Helvetica", 9, "bold"), command=self.controller.show_login_frame, relief="flat", padx=10).pack(side="right", padx=15)
        
        main_layout = tk.Frame(self, bg="#f4f6f9", padx=20, pady=20)
        main_layout.pack(fill="both", expand=True)
        
        config_box = tk.Frame(main_layout, bg="white", bd=1, relief="solid", padx=25, pady=20)
        config_box.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(config_box, text="CẤU HÌNH THÔNG SỐ ĐỀ THI", font=("Helvetica", 12, "bold"), bg="white", fg="#1a73e8").pack(pady=10, anchor="w")
        
        tk.Label(config_box, text="Chọn môn học cần kiểm tra:", bg="white").pack(anchor="w", pady=2)

        self.cbo_subj = ttk.Combobox(config_box, values=["Math", "English", "Vietnamese "], state="readonly", font=("Helvetica", 10))
        self.cbo_subj.pack(fill="x", pady=4); self.cbo_subj.set("Math")
        
        tk.Label(config_box, text="Số lượng câu hỏi (Tròn chục từ 10 - 40):", bg="white").pack(anchor="w", pady=2)
        self.cbo_count = ttk.Combobox(config_box, values=["10", "20", "30", "40"], state="readonly", font=("Helvetica", 10))
        self.cbo_count.pack(fill="x", pady=4); self.cbo_count.set("10")
        
        tk.Label(config_box, text="Ma trận mức độ đề thi (% Dễ - % Vừa - % Khó):", bg="white", font=("Helvetica", 9)).pack(anchor="w", pady=5)
        matrix_presets = [
            "100% Dễ - 0% Vừa - 0% Khó",
            "50% Dễ - 50% Vừa - 0% Khó",
            "50% Dễ - 30% Vừa - 20% Khó",
            "40% Dễ - 40% Vừa - 20% Khó",
            "30% Dễ - 40% Vừa - 30% Khó",
            "0% Dễ - 80% Vừa - 20% Khó",
            "0% Dễ - 50% Vừa - 50% Khó",
            "0% Dễ - 0% Vừa - 100% Khó"
        ]
        self.cbo_matrix = ttk.Combobox(config_box, values=matrix_presets, state="readonly", font=("Helvetica", 10))
        self.cbo_matrix.pack(fill="x", pady=4); self.cbo_matrix.set("50% Dễ - 50% Vừa - 0% Khó")
        
        tk.Label(config_box, text="Thời gian giới hạn ca thi (Phút):", bg="white").pack(anchor="w", pady=2)
        self.cbo_duration = ttk.Combobox(config_box, values=["1", "5", "10", "20", "45", "60"], state="readonly", font=("Helvetica", 10))
        self.cbo_duration.pack(fill="x", pady=4); self.cbo_duration.set("10")
        
        btn_start = tk.Button(config_box, text="🚀 BẮT ĐẦU VÀO PHÒNG THI", font=("Helvetica", 11, "bold"), bg="#2e7d32", fg="white", pady=8, command=self.trigger_generation_exam, relief="flat", cursor="hand2")
        btn_start.pack(fill="x", pady=15)
        
        sidebar = tk.Frame(main_layout, bg="#f4f6f9", width=220)
        sidebar.pack(side="right", fill="y", padx=10)
        
        tk.Button(sidebar, text="🏆 Xem Bảng Xếp Hạng", bg="#ff9800", fg="white", font=("Helvetica", 10, "bold"), pady=12, width=22, relief="flat", command=self.show_leaderboard_frame).pack(pady=8)
        tk.Button(sidebar, text="📜 Xem Lịch Sử Thi", bg="#00bcd4", fg="white", font=("Helvetica", 10, "bold"), pady=12, width=22, relief="flat", command=self.show_history_frame).pack(pady=8)

    def parse_matrix_combobox(self, text_val):
        try:
            parts = text_val.split(" - ")
            easy_p = float(parts[0].split("%")[0]) / 100.0
            med_p = float(parts[1].split("%")[0]) / 100.0
            hard_p = float(parts[2].split("%")[0]) / 100.0
            
            matrix = {}
            if easy_p > 0: matrix["Easy"] = easy_p
            if med_p > 0: matrix["Medium"] = med_p
            if hard_p > 0: matrix["Hard"] = hard_p
            return matrix
        except Exception:
            return {"Easy": 1.0}

    def trigger_generation_exam(self):
        subj = self.cbo_subj.get()
        count = int(self.cbo_count.get())
        duration = int(self.cbo_duration.get())
        diff_matrix = self.parse_matrix_combobox(self.cbo_matrix.get())
        
        # Gọi hàm tạo đề thi từ exam.py
        self.active_exam_data = exam(duration, self.controller.bank, count, subj, diff_matrix)
        
        if not self.active_exam_data.get("questions") or len(self.active_exam_data["questions"]) == 0:
            messagebox.showerror("Thông báo", "Lỗi: Bộ lọc đề thi rỗng! Vui lòng kiểm tra lại file dữ liệu câu hỏi.")
            return
            
        self.render_exam_frame(duration)

    def render_exam_frame(self, duration_mins):
        self.clean_screen()
        
        top_bar = tk.Frame(self, bg="#202124", pady=10, padx=20)
        top_bar.pack(fill="x")
        
        tk.Label(top_bar, text=f"BÀI THI MÔN: {self.active_exam_data['data']['subject'].upper()}", font=("Helvetica", 11, "bold"), fg="#fbbc05", bg="#202124").pack(side="left")
        self.lbl_countdown = tk.Label(top_bar, text="Thời gian: 00:00", font=("Helvetica", 12, "bold"), fg="#ea4335", bg="#202124")
        self.lbl_countdown.pack(side="right")
        
        canvas_pane = tk.Frame(self)
        canvas_pane.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(canvas_pane, bg="#f8f9fa", bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_pane, orient="vertical", command=canvas.yview)
        scroll_content = tk.Frame(canvas, bg="#f8f9fa", padx=35)
        
        # Hàm tự động cập nhật lại vùng cuộn (scrollregion) cho Canvas bất kể đề dài hay ngắn
        def _configure_window(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        scroll_content.bind("<Configure>", _configure_window)
        canvas.create_window((0, 0), window=scroll_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            if canvas.winfo_exists():
                # Lệnh cuộn chuẩn cho Windows và MacOS
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Sử dụng bind_all kết hợp kiểm tra winfo_exists để đảm bảo nhận chuột trên toàn giao diện phòng thi
        self.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Hỗ trợ thêm cuộn chuột cho hệ điều hành Linux (nếu có)
        self.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units") if canvas.winfo_exists() else None)
        self.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units") if canvas.winfo_exists() else None)
        
        self.radio_variables = []
        for idx, q in enumerate(self.active_exam_data["questions"]):
            q_box = tk.Frame(scroll_content, bg="white", bd=1, relief="groove", padx=15, pady=12)
            q_box.pack(fill="x", pady=8)
            
            tk.Label(q_box, text=f"Câu {idx + 1}: {q['text']} [{q['difficulty']}]", font=("Helvetica", 11, "bold"), bg="white", justify="left", anchor="w", wraplength=720).pack(anchor="w", pady=4)
            
            var = tk.StringVar(value="None")
            self.radio_variables.append(var)
            
            for label, choice_text in q["answers"].items():
                tk.Radiobutton(q_box, text=f"{label}. {choice_text}", variable=var, value=label, font=("Helvetica", 10), bg="white", fg="#202124", activebackground="white").pack(anchor="w", padx=20, pady=2)
                
        btn_finish = tk.Button(scroll_content, text="HOÀN THÀNH & NỘP BÀI THI", font=("Helvetica", 11, "bold"), bg="#1a73e8", fg="white", padx=40, pady=10, relief="flat", command=self.handle_manual_submit, cursor="hand2")
        btn_finish.pack(pady=30)
        
        # Ép buộc Tkinter cập nhật lại kích thước nội dung ngay lập tức để tính toán thanh cuộn
        self.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.seconds_remaining = duration_mins * 60
        self.exam_start_time = time.time()
        self.exam_timer_running = True
        self.countdown_tick_logic()

    def countdown_tick_logic(self):
        if not self.exam_timer_running: return
        if self.seconds_remaining <= 0:
            self.lbl_countdown.config(text="Thời gian: 00:00")
            messagebox.showwarning("Hết giờ làm bài", "Đã hết thời gian làm bài quy định! Hệ thống tự động thu bài và chấm điểm.")
            self.execute_scoring_and_render_result()
            return
            
        m, s = divmod(self.seconds_remaining, 60)
        self.lbl_countdown.config(text=f"Thời gian còn lại: {m:02d}:{s:02d}")
        self.seconds_remaining -= 1
        self.after(1000, self.countdown_tick_logic)

    def handle_manual_submit(self):
        if messagebox.askyesno("Xác nhận nộp bài", "Bạn có chắc chắn muốn nộp bài thi ngay bây giờ không?"):
            self.execute_scoring_and_render_result()

    def execute_scoring_and_render_result(self):
        self.exam_timer_running = False
        user_time_spent = int(time.time() - self.exam_start_time)
        answers_collected = [v.get() for v in self.radio_variables]
        
        result_package = results(self.controller.current_user, answers_collected, self.active_exam_data, user_time_spent)
        self.controller.refresh_results_from_disk()
        self.render_result_dashboard(result_package)

    def render_result_dashboard(self, report):
        self.clean_screen()
        
        main_layout = tk.Frame(self, bg="#f4f6f9", padx=20, pady=20)
        main_layout.pack(fill="both", expand=True)
        
        card_score = tk.Frame(main_layout, bg="white", bd=1, relief="solid", pady=15)
        card_score.pack(fill="x", pady=5)
        
        tk.Label(card_score, text="KẾT QUẢ PHÂN TÍCH BÀI THI", font=("Helvetica", 12, "bold"), bg="white", fg="#2e7d32").pack()
        tk.Label(card_score, text=f"{report.get('score')} / 10 Điểm", font=("Helvetica", 20, "bold"), bg="white", fg="#d32f2f").pack(pady=4)
        tk.Label(card_score, text=f"Đúng chính xác: {report.get('correct_count')}/{report.get('total')} câu | Thời gian hoàn thành: {report.get('userTime')} giây", bg="white", font=("Helvetica", 10)).pack()
        
        wrong_panel = tk.Frame(main_layout, bg="white", bd=1, relief="solid", padx=15, pady=10)
        wrong_panel.pack(fill="both", expand=True, pady=10)
        tk.Label(wrong_panel, text="CHI TIẾT CÁC CÂU LÀM CHƯA ĐÚNG", font=("Helvetica", 10, "bold"), bg="white", fg="#c62828").pack(anchor="w")
        
        txt_wrong = tk.Text(wrong_panel, font=("Helvetica", 10), bg="#fafafa", height=12)
        txt_wrong.pack(fill="both", expand=True, pady=5)
        
        uncorrect_list = report.get("uncorrect", [])
        if not uncorrect_list:
            txt_wrong.insert("end", "Hoàn hảo! Bạn trả lời đúng toàn bộ câu hỏi trên đề thi.")
        else:
            for idx, item in enumerate(uncorrect_list, 1):
                txt_wrong.insert("end", f"Lỗi sai {idx}: {item.get('question')}\n")
                txt_wrong.insert("end", f" ❌ Lựa chọn của bạn: {item.get('user_choice') if item.get('user_choice') != 'None' else 'Bỏ trống'}\n")
                txt_wrong.insert("end", f"  ✔ Đáp án chuẩn: {item.get('correct_label')}. {item.get('correct_text')}\n")
                txt_wrong.insert("end", "-"*60 + "\n")
        txt_wrong.config(state="disabled")
        
        tk.Button(main_layout, text="Quay Lại Màn Hình Cấu Hình", font=("Helvetica", 10, "bold"), bg="#555", fg="white", padx=20, pady=6, relief="flat", command=self.render_start_frame).pack(pady=5)

    def show_history_frame(self):
        self.clean_screen()
        self.controller.refresh_results_from_disk()
        
        container = tk.Frame(self, bg="#f4f6f9", padx=25, pady=20)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="LỊCH SỬ KẾT QUẢ THI CỦA BẠN", font=("Helvetica", 12, "bold"), bg="#f4f6f9", fg="#00bcd4").pack(pady=5, anchor="w")
        
        txt_box = tk.Text(container, font=("Helvetica", 10), bg="white")
        txt_box.pack(fill="both", expand=True, pady=10)
        
        my_history = [r for r in self.controller.results_db if r.get("username") == self.controller.current_user]
        
        if not my_history:
            txt_box.insert("end", "Tài khoản của bạn chưa thực hiện bất kỳ ca kiểm tra nào trên hệ thống.")
        else:
            for i, r in enumerate(my_history, 1):
                txt_box.insert("end", f"Lần làm bài {i} [Mã ca: {r.get('exam_id')}] -> Môn: {r.get('subject')}\n")
                txt_box.insert("end", f"Điểm số: {r.get('score')}/10 điểm | Làm mất: {r.get('userTime')} giây\n")
                txt_box.insert("end", "=" * 65 + "\n\n")
                
        txt_box.config(state="disabled")
        tk.Button(container, text="Quay Về Menu Cấu Hình", bg="#555", fg="white", font=("Helvetica", 10, "bold"), padx=15, command=self.render_start_frame, relief="flat").pack(anchor="e")

    def show_leaderboard_frame(self):
        self.clean_screen()
        self.controller.refresh_results_from_disk()
        
        container = tk.Frame(self, bg="#f4f6f9", padx=25, pady=20)
        container.pack(side="top", fill="both", expand=True)
        
        tk.Label(container, text="🏆 BẢNG XẾP HẠNG THÍ SINH ĐIỂM CAO", font=("Helvetica", 12, "bold"), bg="#f4f6f9", fg="#ff9800").pack(pady=5, anchor="w")
        
        # Sắp xếp toàn bộ danh sách kết quả bằng thuật toán bubble_sort có sẵn của ông
        sorted_list = bubble_sort(self.controller.results_db, key=lambda x: x.get("score", 0))
        
        # Khởi tạo thanh Tab (Notebook) để phân tách các môn học
        leaderboard_notebook = ttk.Notebook(container)
        leaderboard_notebook.pack(fill="both", expand=True, pady=10)
        
        # Định nghĩa cấu hình cho 3 môn học (Khớp chính xác chuỗi text lưu trong JSON)
        subjects_config = [
            {"tab_title": "  Môn Toán (Math)  ", "json_name": "Math"},
            {"tab_title": "  Môn Tiếng Anh (English)  ", "json_name": "English"},
            {"tab_title": "  Môn Ngữ Văn (Vietnamese)  ", "json_name": "Vietnamese "}
        ]
        
        columns = ("rank", "exam_id", "user", "score", "time")
        
        # Vòng lặp tự động dựng giao diện bảng cho từng môn
        for sub_item in subjects_config:
            tab_frame = tk.Frame(leaderboard_notebook, bg="white")
            leaderboard_notebook.add(tab_frame, text=sub_item["tab_title"])
            
            # Tạo Treeview riêng cho Tab của môn này
            tree = ttk.Treeview(tab_frame, columns=columns, show="headings")
            tree.heading("rank", text="Hạng")
            tree.heading("exam_id", text="Mã Ca Thi")
            tree.heading("user", text="Tên Thí Sinh")
            tree.heading("score", text="Điểm Số")
            tree.heading("time", text="Thời Gian làm")
            
            tree.column("rank", width=60, anchor="center")
            tree.column("exam_id", width=100, anchor="center")
            tree.column("score", width=100, anchor="center")
            tree.column("time", width=120, anchor="center")
            tree.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Lọc dữ liệu kết quả thi và đổ vào bảng tương ứng của từng môn
            rank_counter = 1
            for item in sorted_list:
                # Ép kiểu chuỗi về chữ thường và xóa khoảng trắng để lọc chính xác tuyệt đối
                if item.get("subject", "").strip().lower() == sub_item["json_name"].strip().lower():
                    tree.insert(
                        "", "end", 
                        values=(
                            rank_counter, 
                            item.get("exam_id"), 
                            item.get("username"), 
                            f"{item.get('score')} / 10", 
                            f"{item.get('userTime')} giây"
                        )
                    )
                    rank_counter += 1
                    
        # Nút quay về giao diện cấu hình ban đầu
        tk.Button(container, text="🏠 Quay Về Màn Hình Chính", bg="#555", fg="white", font=("Helvetica", 10, "bold"), padx=15, pady=6, command=self.render_start_frame, relief="flat", cursor="hand2").pack(anchor="e", pady=5)