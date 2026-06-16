from core import datahand
from core.exam import exam, results

def main():
    print("=== HỆ THỐNG THI TRẮC NGHIỆM ===")

    # 1. Nạp ngân hàng câu hỏi từ file questions.json
    bank = datahand.loadData(datahand.QUESTIONS_FILE)
    if not bank:
        print(" Lỗi: Ngân hàng câu hỏi trống hoặc không tìm thấy file!")
        return

    print(f" Đã nạp thành công {len(bank)} câu hỏi từ hệ thống.\n")

    # 2. Nhập thông tin cấu hình đề thi từ bàn phím
    print("--- BƯỚC 1: CẤU HÌNH ĐỀ THI ---")
    subj_test = input(" Nhập môn học muốn thi (VD: Toan, Vietnamese, English): ").strip()
    
    try:
        count = int(input(" Nhập số lượng câu hỏi muốn tạo: "))
    except ValueError:
        print(" Lỗi: Số lượng câu hỏi bắt buộc phải là một số nguyên!")
        return

    dur_time = input(" Nhập thời gian làm bài (VD: 45 phút, 60 phút): ").strip()

    diff_matrix = {"Easy": 0.5, "Medium" :0.3, "Hard": 0.2}

    print(f"\n Đang tiến hành sinh đề: Môn {subj_test} | {count} câu | Thời gian: {dur_time}...")
    
    # 3. Kích hoạt hàm sinh đề thi
    exam_package = exam(dur_time=dur_time, bank=bank, count=count, subj=subj_test, diff_matrix=diff_matrix)
    
    total_generated = exam_package['data']['count']
    if total_generated == 0:
        print(" Lỗi: Không tìm thấy câu hỏi nào khớp với môn học đã chọn!")
        return
        
    print(f" Sinh đề thành công! Số câu thực tế lấy được: {total_generated} câu.\n")

    # 4. Giao diện thi thử nghiệm trên Terminal
    print("--- BƯỚC 2: MÔ PHỎNG LÀM BÀI THI ---")
    print(f"⏱️ Thời gian bắt đầu tính: {dur_time}. Hãy nhập đáp án của ông.")
    
    user_answers = []
    
    for i, q in enumerate(exam_package['questions']):
        print(f"\nCâu {i+1}: {q['text']}")
        # In các lựa chọn A, B, C, D đã bị xáo trộn
        for label, text in q['answers'].items():
            print(f"   {label}. {text}")
        
        # Cho phép người thử nghiệm nhập đáp án thật
        ans = input("Nhập đáp án của bạn (A/B/C/D) hoặc nhấn Enter để bỏ qua: ").strip().upper()
        
        # Nếu nhập bậy hoặc bỏ trống thì ghi nhận là None (bỏ trống)
        if ans in ['A', 'B', 'C', 'D']:
            user_answers.append(ans)
        else:
            user_answers.append(None)

    print("\n Đã hoàn thành bài thi! Đang tiến hành nộp bài và chấm điểm...")

    # 5. Chấm điểm và ghi nhận vào results.json
    result = results(username="Dung_Tester", user_answers=user_answers, exam_data=exam_package, userTime="Hoàn thành")

    # 6. Hiển thị bảng điểm tổng kết
    print("\n=== BẢNG ĐIỂM KẾT QUẢ CHI TIẾT ===")
    print(f" Mã ca thi   : {result['exam_id']}")
    print(f" Thí sinh    : {result['username']}")
    print(f" Số câu đúng : {result['correct_count']}/{result['total']}")
    print(f" Điểm số     : {result['score']} / 10 điểm")
    print(f" Trạng thái  : {result['status']} (Chờ Admin duyệt)")
    print("==================================")
    
    # 7. Báo cáo chi tiết các câu làm sai (Mới cập nhật)
    if len(result['uncorrect']) == 0:
        print(" Xuất sắc! Điểm tuyệt đối!")
    else:
        print(f" DANH SÁCH {len(result['uncorrect'])} CÂU HỎI LÀM SAI VÀ ĐÁP ÁN ĐÚNG:")
        print("-" * 50)
        for idx, item in enumerate(result['uncorrect']):
            print(f"Câu sai số {idx+1}: {item['question']}")
            print(f"    Đáp án bạn chọn: {item['user_choice'] if item['user_choice'] else 'Bỏ trống'}")
            print(f"    Đáp án đúng của hệ thống: {item['correct_label']}. {item['correct_text']}")
            print("-" * 50)

    print("\n✅ Đã ghi nhận nhật ký thi xuống tệp data/results.json!")

if __name__ == "__main__":
    main()