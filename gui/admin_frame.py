import tkinter as tk
from tkinter import ttk, messagebox
from core import datahand          
from core.algorithms import bubble_sort 

class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.controller.refresh_results_from_disk()
        
        # Header điều hướng
        header = tk.Frame(self, bg="#202124", pady=10)
        header.pack(fill="x")
        tk.Label(header, text="GIAO DIỆN QUẢN TRỊ CỦA GIÁO VIÊN", font=("Helvetica", 11, "bold"), fg="white", bg="#202124").pack(side="left", padx=15)
        tk.Button(header, text="Đăng xuất", bg="#d32f2f", fg="white", font=("Helvetica", 9, "bold"), command=self.controller.show_login_frame, relief="flat", padx=12).pack(side="right", padx=15)
        
        # Tabs hệ thống
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab1 = tk.Frame(notebook, bg="#f8f9fa")
        self.tab2 = tk.Frame(notebook, bg="#f8f9fa")
        notebook.add(self.tab1, text="  Thêm Câu Hỏi Mới  ")
        notebook.add(self.tab2, text="  Quản Lý Kết Quả & Câu Sai  ")
        
        self.setup_tab1()
        self.setup_tab2()

    # --- TAB 1: THÊM CÂU HỎI MỚI ---
    def setup_tab1(self):
        pad_frame = tk.Frame(self.tab1, bg="#f8f9fa", padx=20, pady=20)
        pad_frame.pack(fill="both", expand=True)
        
        tk.Label(pad_frame, text="Môn học:", bg="#f8f9fa", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=6)
        self.subj_var = tk.StringVar(value="Toan")
        ttk.Combobox(pad_frame, textvariable=self.subj_var, values=["Toan", "English", "Vietnamese "], state="readonly", width=20).grid(row=0, column=1, sticky="w")
        
        tk.Label(pad_frame, text="Mức độ khó:", bg="#f8f9fa", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="w", pady=6)
        self.diff_var = tk.StringVar(value="Easy")
        ttk.Combobox(pad_frame, textvariable=self.diff_var, values=["Easy", "Medium", "Hard"], state="readonly", width=20).grid(row=1, column=1, sticky="w")
        
        tk.Label(pad_frame, text="Nội dung câu hỏi:", bg="#f8f9fa", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky="nw", pady=6)
        self.txt_text = tk.Text(pad_frame, height=4, width=55, font=("Helvetica", 10))
        self.txt_text.grid(row=2, column=1, sticky="w", pady=6)
        
        self.ans_entries = {}
        for idx, label in enumerate(["A", "B", "C", "D"]):
            tk.Label(pad_frame, text=f"Đáp án {label}:", bg="#f8f9fa").grid(row=3+idx, column=0, sticky="w", pady=4)
            e = tk.Entry(pad_frame, width=50, font=("Helvetica", 10))
            e.grid(row=3+idx, column=1, sticky="w", pady=4)
            self.ans_entries[label] = e
            
        tk.Label(pad_frame, text="Đáp án đúng:", bg="#f8f9fa", font=("Helvetica", 10, "bold")).grid(row=7, column=0, sticky="w", pady=6)
        self.correct_var = tk.StringVar(value="A")
        ttk.Combobox(pad_frame, textvariable=self.correct_var, values=["A", "B", "C", "D"], state="readonly", width=10).grid(row=7, column=1, sticky="w")
        
        tk.Button(pad_frame, text="Lưu Câu Hỏi Vào Ngân Hàng", bg="#2e7d32", fg="white", font=("Helvetica", 10, "bold"), pady=6, padx=15, relief="flat", command=self.save_new_question).grid(row=8, column=1, sticky="e", pady=15)

    def save_new_question(self):
        text_content = self.txt_text.get("1.0", "end").strip()
        if not text_content or any(not self.ans_entries[l].get().strip() for l in ["A", "B", "C", "D"]):
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng không bỏ trống nội dung câu hỏi và 4 đáp án!")
            return
            
        new_q = {
            "id": 0, 
            "subject": self.subj_var.get(),
            "difficulty": self.diff_var.get(),
            "text": text_content,
            "answers": {l: self.ans_entries[l].get().strip() for l in ["A", "B", "C", "D"]},
            "correct_label": self.correct_var.get()
        }
        
        if datahand.updateData(datahand.QUESTIONS_FILE, new_q):
            self.controller.bank = datahand.loadData(datahand.QUESTIONS_FILE) 
            messagebox.showinfo("Thành công", "Đã thêm câu hỏi mới thành công vào tệp dữ liệu!")
            self.txt_text.delete("1.0", "end")
            for entry in self.ans_entries.values(): entry.delete(0, "end")

    # --- TAB 2: QUẢN LÝ KẾT QUẢ ---
    def setup_tab2(self):
        left_pane = tk.Frame(self.tab2, bg="#f8f9fa", padx=10, pady=10)
        left_pane.pack(side="left", fill="both", expand=True)
        
        right_pane = tk.Frame(self.tab2, bg="white", width=340, bd=1, relief="solid", padx=15, pady=10)
        right_pane.pack(side="right", fill="y")
        right_pane.pack_propagate(False)
        
        columns = ("exam_id", "user", "sub", "score")
        self.tree = ttk.Treeview(left_pane, columns=columns, show="headings")
        self.tree.heading("exam_id", text="Mã Ca Thi"); self.tree.heading("user", text="Thí Sinh")
        self.tree.heading("sub", text="Môn Thi"); self.tree.heading("score", text="Điểm Số")
        
        self.tree.column("exam_id", width=100, anchor="center")
        self.tree.column("score", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_result)
        
        self.lbl_selected = tk.Label(right_pane, text="Ca thi: Chưa lựa chọn", font=("Helvetica", 10, "bold"), bg="white", fg="#1a73e8")
        self.lbl_selected.pack(anchor="w", pady=5)
        
        tk.Label(right_pane, text="Phân tích chi tiết các câu sai:", font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w", pady=5)
        self.txt_wrong_box = tk.Text(right_pane, height=22, width=40, bg="#f1f3f4", font=("Helvetica", 9), state="disabled")
        self.txt_wrong_box.pack(fill="both", expand=True, pady=5)
        
        self.refresh_results_tree()

    def refresh_results_tree(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for idx, res in enumerate(self.controller.results_db):
            self.tree.insert("", "end", iid=str(idx), values=(res.get("exam_id"), res.get("username"), res.get("subject"), f"{res.get('score')}/10"))

    def on_select_result(self, event):
        selected = self.tree.selection()
        if not selected: return
        self.current_selected_index = int(selected[0])
        res_data = self.controller.results_db[self.current_selected_index]
        
        self.lbl_selected.config(text=f"Mã: {res_data.get('exam_id')} - Học sinh: {res_data.get('username')}")
        
        self.txt_wrong_box.config(state="normal")
        self.txt_wrong_box.delete("1.0", "end")
        uncorrect_list = res_data.get("uncorrect", [])
        if not uncorrect_list:
            self.txt_wrong_box.insert("end", "Thí sinh làm đúng 100%! Không có câu sai.")
        else:
            for c_idx, item in enumerate(uncorrect_list, 1):
                self.txt_wrong_box.insert("end", f"Câu sai {c_idx}: {item.get('question')}\n")
                self.txt_wrong_box.insert("end", f" -> Học sinh chọn: {item.get('user_choice')} | Đúng: {item.get('correct_label')}. {item.get('correct_text')}\n\n")
        
        self.txt_wrong_box.config(state="disabled")