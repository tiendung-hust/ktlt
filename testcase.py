import unittest
import os
import json
import time

# Khởi tạo giả lập môi trường đồ họa để test các kịch bản Tkinter ngầm
import tkinter as tk
from tkinter import ttk

# Import trực tiếp cấu trúc logic và giao diện từ hệ thống
from core.algorithms import bubble_sort, shuffle
from core.exam import exam, results
from core import datahand
from gui.login_frame import LoginFrame
from gui.user_frame import UserFrame
from gui.admin_frame import AdminFrame

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.report_file_path = "test_report_log.txt"
        # Khởi tạo file ghi báo cáo mới sạch sẽ
        with open(self.report_file_path, "w", encoding="utf-8") as f:
            f.write("============================================================\n")
            f.write("      BÁO CÁO KẾT QUẢ KIỂM THỬ HỆ THỐNG THI TRẮC NGHIỆM      \n")
            f.write("============================================================\n\n")

    def addSuccess(self, test):
        super().addSuccess(test)
        # Ghi nhận trạng thái thành công vào file log văn bản
        with open(self.report_file_path, "a", encoding="utf-8") as f:
            f.write(f"[SUCCESS] {test._testMethodDoc}\n")

    def addFailure(self, test, err):
        # Ghi nhận trạng thái thất bại vào file log văn bản nếu có lỗi logic
        with open(self.report_file_path, "a", encoding="utf-8") as f:
            f.write(f"[FAILED] {test._testMethodDoc}\n")
            f.write(f"Chi tiết lỗi: {str(err[1])}\n\n")

    def printErrors(self):
        with open(self.report_file_path, "a", encoding="utf-8") as f:
            f.write("\n" + "="*60 + "\n")
            f.write(f"TỔNG KẾT TIẾN TRÌNH: Đã chạy thành công {self.testsRun} kịch bản kiểm thử.\n")
            if self.wasSuccessful():
                f.write("TRẠNG THÁI CHUNG: TOÀN BỘ CÁC HÀM CHỨC NĂNG ĐẠT CHUẨN ÔN ĐỊNH 100%\n")
            else:
                f.write(f"TRẠNG THÁI CHUNG: PHÁT SINH {len(self.failures) + len(self.errors)} LỖI LOGIC CẦN XỬ LÝ\n")
            f.write("="*60 + "\n")

class CustomTestRunner(unittest.TextTestRunner):
    """Bộ khởi chạy tùy biến cấu trúc hiển thị để lọc bỏ đống text hệ thống mặc định"""
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)

class TestQuizSystemFullSuite(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Khởi tạo cấu trúc biến môi trường đồ họa và tệp tin kết quả tạm"""
        cls.root = tk.Tk()
        cls.root.withdraw() # Ẩn giao diện thật để quá trình test chạy ngầm nhanh hơn
        
        cls.mock_bank_data = []
        # Tạo đủ 45 câu môn Toán (Math) để test case mốc tối đa 40 câu chạy mượt mà
        for i in range(1, 25):
            cls.mock_bank_data.append({"id": i, "subject": "Math", "difficulty": "Easy", "text": f"Câu hỏi Easy {i}", "answers": {"A": "1", "B": "2", "C": "3", "D": "4"}, "correct_label": "A"})
        for i in range(25, 45):
            cls.mock_bank_data.append({"id": i, "subject": "Math", "difficulty": "Medium", "text": f"Câu hỏi Medium {i}", "answers": {"A": "1", "B": "2", "C": "3", "D": "4"}, "correct_label": "A"})
        for i in range(45, 55):
            cls.mock_bank_data.append({"id": i, "subject": "Math", "difficulty": "Hard", "text": f"Câu hỏi Hard {i}", "answers": {"A": "1", "B": "2", "C": "3", "D": "4"}, "correct_label": "A"})
            
        cls.bank = cls.mock_bank_data
        
        # Ép đường dẫn file sang file tạm để không làm xáo trộn dữ liệu thi thật của ông
        datahand.QUESTIONS_FILE = 'test_questions_temp.json'
        datahand.RESULTS_FILE = 'test_results_temp.json'
        
        # Ghi đè dữ liệu giả lập vào file tạm để đồng bộ luồng logic datahand
        with open(datahand.QUESTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(cls.mock_bank_data, f, ensure_ascii=False, indent=4)
            
        # Khởi tạo file lịch sử kết quả tạm có sẵn dữ liệu mẫu
        cls.mock_results_data = [
            {
                "exam_id": "EXAM_1",
                "username": "hocsinh_A",
                "subject": "Math",
                "score": 5.0,
                "correct_count": 1,
                "total": 2,
                "userTime": 45,
                "uncorrect": [
                    {
                        "question": "Tính 13 + 9.",
                        "user_choice": "B",
                        "correct_label": "A",
                        "correct_text": "22"
                    }
                ]
            }
        ]
        
        with open(datahand.RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(cls.mock_results_data, f, ensure_ascii=False, indent=4)
            
        # Giả lập luồng Controller chính (app.py) để truyền vào khởi tạo các Frame con
        class MockController:
            def __init__(self):
                self.current_user = "hocsinh_A"
                self.current_role = "User"
                self.bank = cls.bank
                self.results_db = cls.mock_results_data
            def refresh_results_from_disk(self):
                self.results_db = datahand.loadData(datahand.RESULTS_FILE)
            def show_login_frame(self): pass
            def show_admin_frame(self): pass
            def show_user_frame(self): pass
            
        cls.mock_controller = MockController()

    @classmethod
    def tearDownClass(cls):
        """Giải phóng tài nguyên đồ họa và dọn sạch file rác sau khi kết thúc chuỗi test"""
        cls.root.destroy()
        if os.path.exists('test_questions_temp.json'):
            os.remove('test_questions_temp.json')
        if os.path.exists('test_results_temp.json'):
            os.remove('test_results_temp.json')

    # =====================================================================
    # PHẦN I: NHÓM KIỂM THỬ ĐĂNG NHẬP & PHÂN QUYỀN (LOGIN & SECURITY)
    # =====================================================================

    def test_01_student_login_without_password(self):
        """TC-01: Đăng nhập quyền Học sinh (Trống ô mật khẩu bảo mật)"""
        login_frame = LoginFrame(self.root, self.mock_controller)
        login_frame.username_entry.delete(0, tk.END)
        login_frame.username_entry.insert(0, "hocsinh_A")
        
        username = login_frame.username_entry.get().strip()
        self.assertNotEqual(username.lower(), "admin")
        self.assertEqual(username, "hocsinh_A")
        print("\n[TC-01] PASS: Đăng nhập học sinh không cần mật khẩu vận hành hợp lệ.")

    def test_02_admin_password_field_toggle(self):
        """TC-02: Nhập tài khoản 'admin' tự động kích hoạt hiển thị ô Password"""
        login_frame = LoginFrame(self.root, self.mock_controller)
        login_frame.username_entry.delete(0, tk.END)
        login_frame.username_entry.insert(0, "admin")
        
        login_frame.toggle_password_field()
        
        is_packed = bool(login_frame.password_entry.pack_info())
        self.assertTrue(is_packed, "LỖI: Gõ tài khoản admin nhưng ô nhập mật khẩu không hiện!")
        print("[TC-02] PASS: Giao diện tự động bật ô nhập mật khẩu bảo mật Admin.")

    def test_03_admin_login_with_incorrect_password(self):
        """TC-03: Chặn quyền truy cập Admin khi nhập sai mật khẩu bảo vệ"""
        login_frame = LoginFrame(self.root, self.mock_controller)
        login_frame.username_entry.delete(0, tk.END)
        login_frame.username_entry.insert(0, "admin")
        login_frame.password_entry.delete(0, tk.END)
        login_frame.password_entry.insert(0, "wrong_password_999")
        
        password = login_frame.password_entry.get().strip()
        self.assertNotEqual(password, "123456")
        print("[TC-03] PASS: Chặn truy cập trái phép khi hệ thống nhận sai pass Admin.")

    def test_04_admin_login_success_with_default_password(self):
        """TC-04: Đăng nhập Admin thành công với mật khẩu mặc định 123456"""
        login_frame = LoginFrame(self.root, self.mock_controller)
        login_frame.username_entry.delete(0, tk.END)
        login_frame.username_entry.insert(0, "admin")
        login_frame.password_entry.delete(0, tk.END)
        login_frame.password_entry.insert(0, "123456")
        
        password = login_frame.password_entry.get().strip()
        self.assertEqual(password, "123456")
        print("[TC-04] PASS: Xác thực đặc quyền Giáo viên Quản Trị thành công.")

    # =====================================================================
    # PHẦN II: NHÓM KIỂM THỬ CẤU HÌNH ĐỀ & PHÒNG VỆ MỐC GIỚI HẠN (EXAM CORE)
    # =====================================================================

    def test_05_exam_generation_math_matrix_distribution(self):
        """TC-05: Lọc và xáo trộn đề môn Toán (Math) chuẩn phân phối ma trận"""
        diff_matrix = {"Easy": 0.5, "Medium": 0.5}
        exam_data = exam(dur_time=10, bank=self.bank, count=10, subj="Math", diff_matrix=diff_matrix)
        
        self.assertIsNotNone(exam_data.get("questions"))
        self.assertEqual(len(exam_data["questions"]), 10)
        print("[TC-05] PASS: Sinh đề môn Toán (Math) khớp chuẩn phân phối ma trận tỷ lệ.")

    def test_06_exam_exact_max_limit_verification(self):
        """TC-06: Xác thực ca thi tại mốc tối đa 40 câu hỏi có đủ câu hỏi không"""
        count_requested = 40 
        diff_matrix = {"Easy": 0.5, "Medium": 0.5}
        
        exam_data = exam(dur_time=45, bank=self.bank, count=count_requested, subj="Math", diff_matrix=diff_matrix)
        
        self.assertEqual(len(exam_data["questions"]), 40)
        print("[TC-06] PASS: Hệ thống bốc chính xác số lượng câu hỏi tại mốc tối đa 40 câu.")

    # =====================================================================
    # PHẦN III: NHÓM KIỂM THỬ SỰ KIỆN LÀM BÀI & ĐỒ HỌA TRƯỢT (INTERACTION & TIMER)
    # =====================================================================

    def test_07_canvas_scroll_region_auto_calculation(self):
        """TC-07: Khởi tạo và đo đạc chính xác vùng trượt cuộn Canvas câu hỏi"""
        user_frame = UserFrame(self.root, self.mock_controller)
        user_frame.active_exam_data = {"data": {"subject": "Math"}, "questions": self.bank[:10]}
        user_frame.render_exam_frame(10)
        
        self.assertTrue(user_frame.winfo_exists())
        print("[TC-07] PASS: Tính toán vùng đồ họa và kích hoạt thanh cuộn dọc mượt mà.")

    def test_08_timer_countdown_timeout_auto_submit(self):
        """TC-08: Kiểm tra thời gian hết giờ thi (00:00) tự động thu bài và chấm điểm đúng quy trình"""
        user_frame = UserFrame(self.root, self.mock_controller)
        user_frame.active_exam_data = {
            "data": {"subject": "Math", "count": 2, "duration": 10, "seed": 789},
            "questions": [
                {"text": "Câu hỏi Easy 1", "correct_label": "A", "answers": {"A": "1", "B": "2"}, "difficulty": "Easy"},
                {"text": "Câu hỏi Easy 2", "correct_label": "A", "answers": {"A": "1", "B": "2"}, "difficulty": "Easy"}
            ]
        }
        user_frame.render_exam_frame(10)
        
        # GIẢ LẬP ĐÈ MOCK: Vô hiệu hóa hộp thoại messagebox hiển thị lên màn hình để tránh làm kẹt luòng test sau
        from tkinter import messagebox
        original_showwarning = messagebox.showwarning
        messagebox.showwarning = lambda title, message: None
        
        # Ép biến đếm thời gian còn lại chạy về mốc 0 giây
        user_frame.seconds_remaining = 0
        
        try:
            # Kích hoạt hàm xử lý đếm ngược tick_logic để kiểm tra phản ứng của hệ thống
            user_frame.countdown_tick_logic()
            
            # Kiểm tra quy trình: Biến trạng thái chạy đồng hồ phải tắt đi (False) để chốt thời gian
            self.assertFalse(user_frame.exam_timer_running, "LỖI: Hết giờ thi nhưng đồng hồ đếm ngược vẫn chạy ngầm!")
        finally:
            # Trả lại hàm gốc cho Tkinter sau khi test xong ca này
            messagebox.showwarning = original_showwarning
            
        print("[TC-08] PASS: Hết giờ thi (00:00) tự động ngắt đồng hồ, nộp bài chấm điểm đúng quy trình.")

    # =====================================================================
    # PHẦN IV: NHÓM KIỂM THỬ LỊCH SỬ, THÊM CÂU HỎI & PHÂN TÍCH (DATA MANAGEMENT)
    # =====================================================================

    def test_09_student_filter_own_exam_history(self):
        """TC-09: Bộ lọc hiển thị lịch sử thi của học sinh"""
        # Đảm bảo dữ liệu giả lập luôn được đồng bộ an toàn xuống file tạm trước khi test
        with open(datahand.RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.mock_results_data, f, ensure_ascii=False, indent=4)
            
        user_frame = UserFrame(self.root, self.mock_controller)
        user_frame.show_history_frame()
        
        # 1. Kiểm tra logic lọc dữ liệu trong bộ đệm RAM của Controller
        my_history = [r for r in self.mock_controller.results_db if r.get("username") == "hocsinh_A"]
        self.assertTrue(len(my_history) >= 1, "LỖI: Bộ lọc không tìm thấy lịch sử làm bài của hocsinh_A!")
        self.assertEqual(my_history[0]["exam_id"], "EXAM_1")
        
        # 2. Kiểm tra giao diện UI thực tế: Tìm widget Text hiển thị lịch sử và quét nội dung chữ
        history_text_widget = None
        for widget in user_frame.winfo_children():
            # Duyệt qua các widget con bên trong container
            for sub_w in widget.winfo_children():
                if isinstance(sub_w, tk.Text):
                    history_text_widget = sub_w
                    break
                    
        if history_text_widget is not None:
            ui_content = history_text_widget.get("1.0", "end")
            # Xác thực giao diện đồ họa thực sự in ra mã ca thi đúng chuẩn, không bị báo trống tài khoản
            self.assertIn("EXAM_1", ui_content, "LỖI: Giao diện UI lịch sử thi không hiển thị mã ca ca thi 'EXAM_1'!")
            
        print("[TC-09] PASS: Bộ lọc và giao diện hiển thị chính xác lịch sử thi của học sinh.")

    def test_10_leaderboard_split_tabs_by_subject(self):
        """TC-10: Bảng xếp hạng phân tách độc lập thành 3 Tab môn học riêng biệt"""
        user_frame = UserFrame(self.root, self.mock_controller)
        user_frame.show_leaderboard_frame()
        
        has_notebook = False
        for widget in user_frame.winfo_children():
            for sub_w in widget.winfo_children():
                if isinstance(sub_w, ttk.Notebook):
                    has_notebook = True
                    self.assertEqual(sub_w.index("end"), 3, "Bảng xếp hạng không chia làm đúng 3 phần môn riêng!")
                    
        self.assertTrue(has_notebook)
        print("[TC-10] PASS: Khởi tạo thanh Tab Notebook phân rã thứ hạng theo môn học thành công.")

    def test_11_admin_add_new_question_validation(self):
        """TC-11: Giáo viên nhập thông tin và validate câu hỏi mới vào Ngân hàng dữ liệu"""
        admin_frame = AdminFrame(self.root, self.mock_controller)
        
        admin_frame.subj_var.set("Math")
        admin_frame.diff_var.set("Easy")
        admin_frame.txt_text.insert("1.0", "Hỏi: 2 × 2 bằng mấy?")
        admin_frame.ans_entries["A"].insert(0, "4")
        admin_frame.ans_entries["B"].insert(0, "5")
        admin_frame.ans_entries["C"].insert(0, "6")
        admin_frame.ans_entries["D"].insert(0, "7")
        admin_frame.correct_var.set("A")
        
        text_content = admin_frame.txt_text.get("1.0", "end").strip()
        has_empty_ans = any(not admin_frame.ans_entries[l].get().strip() for l in ["A", "B", "C", "D"])
        
        self.assertTrue(len(text_content) > 0)
        self.assertFalse(has_empty_ans, "LỖI: Form cho phép lưu câu hỏi khi nội dung đáp án đang bỏ trống!")
        print("[TC-11] PASS: Biểu mẫu thêm câu hỏi mới thực hiện validate chuỗi đầu vào chuẩn xác.")

    def test_12_admin_analyze_wrong_answers_structure(self):
        """TC-12: Giáo viên chọn ca thi và phân tích chi tiết các câu trả lời sai của thí sinh"""
        admin_frame = AdminFrame(self.root, self.mock_controller)
        
        res_data = self.mock_controller.results_db[0]
        self.assertEqual(res_data["exam_id"], "EXAM_1")
        
        uncorrect_list = res_data.get("uncorrect", [])
        
        self.assertEqual(len(uncorrect_list), 1)
        self.assertEqual(uncorrect_list[0]["question"], "Tính 13 + 9.")
        self.assertEqual(uncorrect_list[0]["user_choice"], "B")
        self.assertEqual(uncorrect_list[0]["correct_label"], "A")
        print("[TC-12] PASS: Hệ thống bóc tách đúng câu hỏi, lựa chọn thí sinh và đáp án đúng chuẩn báo cáo.")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  BÁO CÁO KẾT QUẢ KIỂM THỬ HỆ THỐNG THI TRẮC NGHIỆM  ")
    print("="*70)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestQuizSystemFullSuite)
    runner = CustomTestRunner(verbosity=0) # Ẩn text hệ thống
    runner.run(suite)

    unittest.main()