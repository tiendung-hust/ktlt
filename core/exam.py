from core.algorithms import shuffle
from core import datahand  
import time

# Hàm tạo đề thi được xáo trộn câu hỏi và đáp án
def exam(dur_time, bank, count, subj, diff_matrix):
    # Lấy seed từ thời gian thực
    seed = int(time.time() * 1000)   

    # Khởi tạo mảng rỗng, lưu câu hỏi
    ex_ques = []                 

    # Lấy câu hỏi phụ thuộc vào độ khó và tỉ lệ các câu hỏi khó, dễ
    for diff, tile in diff_matrix.items():  
        # Số câu hỏi của mức độ diff = số câu hỏi người dùng chọn nhân với tỉ lệ
        num_ques = int(count * tile)
        
        # Lấy câu hỏi từ bank
        filtered = [q for q in bank if q['subject'] == subj and q['difficulty'] == diff]
        
        if len(filtered) < num_ques:
            print(f"Cảnh báo: Không đủ câu hỏi cho độ khó {diff}")
            num_ques = len(filtered)  
        
        # Xáo trộn các câu hỏi vừa chọn
        shuffled = shuffle(filtered, seed)
        
        # Nạp câu hỏi vào đề thi
        ex_ques.extend(shuffled[:num_ques])                
    
    # Xáo trộn lại đề thi lần cuối
    final_shuffle = shuffle(ex_ques, seed)                    

    for q in final_shuffle:
        labels = list(q['answers'].keys())                
        values = list(q['answers'].values())                
    
        correct_text = q['answers'][q['correct_label']]     
        
        # Xáo trộn nội dung các đáp án 
        shuffled_values = shuffle(values, seed)            
        
        # Khởi tạo dict mới, lưu câu hỏi sau khi xáo trộn
        new_answers = {}                                    
        
        for i in range(len(labels)):
            current_label = labels[i]        
            shuffled_value = shuffled_values[i] 
            
            # Ghép nội dung đáp án vào các đáp án A,B,C,D mới
            new_answers[current_label] = shuffled_value     
        
        # Cập nhật từ điển đáp án vào câu hỏi   
        q['answers'] = new_answers                          
        
        # Kiểm tra đáp án đúng
        for label, text in q['answers'].items():            
            if text == correct_text:
                q['correct_label'] = label
                break

    return {
        "data": {
            "subject": subj,
            "count": len(final_shuffle),  # Cập nhật số lượng thực tế
            "duration": dur_time,
            "seed": seed
        },
        "questions": final_shuffle
    } 

# Hàm trả về điểm thi và các câu trả lời sai để phục vụ báo cáo và xếp hạng
def results(username, user_answers, exam_data, userTime):

    correct_count = 0
    uncorrect_ques = []

    for i, q in enumerate(exam_data['questions']):
        # Lấy đáp án người dùng chọn (mặc định là None nếu họ bỏ trống)
        if i < len(user_answers):                                               
            user_choice = user_answers[i]                                     
        else: 
            user_choice = None 
      
        correct_label = q['correct_label']
        
        # So sánh đáp án người dùng chọn với đáp án đúng
        if user_choice == correct_label:                                     
            correct_count += 1
        else:
            # Ghi lại chi tiết để phân tích lỗi sai
            uncorrect_ques.append({                                           
                "question": q['text'],
                "user_choice": user_choice,
                "correct_label": correct_label,
                "correct_text": q['answers'].get(correct_label, "N/A")
            })
            
    total = len(exam_data['questions'])

    if total > 0:
        score = (correct_count / total) * 10  
    else:       
        score = 0
        
    # Đọc file lịch sử để xem hiện tại đang có bao nhiêu bài thi
    history_data = datahand.loadData(datahand.RESULTS_FILE)
    
    if len(history_data) == 0:
        exam_id = "EXAM_1"
    else:
        #Lấy mã ca thi của người nộp bài gần nhất (phần tử cuối mảng)
        last_record = history_data[-1]
        last_id_str = last_record.get("exam_id", "EXAM_0") # Trả về dạng "EXAM_X"
        
        last_num = int(last_id_str.split("_")[1])
        exam_id = f"EXAM_{last_num + 1}"
    
    # Đóng gói khối dữ liệu kết quả 
    result_package = {
        "exam_id": exam_id,
        "username": username,
        "score": round(score, 2),
        "correct_count": correct_count,
        "total": total,
        "userTime": userTime,
        "uncorrect": uncorrect_ques,
        "status": "pending",         # Trạng thái chờ giáo viên chấm bài
        "teacher_comment": None      # Mặc định lời phê để trống
    }
    
    # Kích hoạt lưu thẳng kết quả xuống file JSON
    datahand.updateData(datahand.RESULTS_FILE, result_package)
    
    return result_package