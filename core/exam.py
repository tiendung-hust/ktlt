from algorithms import shuffle
import time

def exam(dur_time, bank, count, subj, diff_matrix):

    seed=int(time.time()*1000)   #Lấy từ thời gian thực

    ex_ques=[]                   #Khởi tạo mảng rỗng, lưu câu hỏi

    for diff, tile in diff_matrix.items():                  #Lấy câu hỏi phụ thuộc vào độ khó và tỉ lệ các câu hỏi khó, dễ

        num_ques=int(count*tile)

        filtered=[q for q in bank if q['subject']==subj and q['difficulty']==diff]

        if len(filtered) < num_ques:
        
            print(f"Cảnh báo: Không đủ câu hỏi cho độ khó {diff}")

        shuffled=shuffle(filtered,seed)

        ex_ques.extend(shuffled[:num_ques])                 #Nạp câu hỏi vào đề thi

    final_shuffle=shuffle(ex_ques,seed)                     #Xáo trộn lại đề thi lần cuối


    for q in final_shuffle:
        labels = list(q['answers'].keys())                  #A,B,C,D
        values = list(q['answers'].values())                #Nội dung đáp án
    
        correct_text = q['answers'][q['correct_label']]     
        
        shuffled_values = shuffle(values, seed)             #Xáo trộn các đáp án 
        
        new_answers = {}                                    #Khởi tạo dict mới, lưu câu hỏi sau khi xáo trộn
        
        for i in range(len(labels)):
            current_label = labels[i]         
            shuffled_value = shuffled_values[i] 
            
            new_answers[current_label] = shuffled_value     #Ghép nội dung đáp án vào các đáp án A,B,C,D mới
            
        q['answers'] = new_answers                          #Cập nhật từ điển đáp án vào câu hỏi
        
        for label, text in q['answers'].items():            #Kiểm tra đáp án đúng
            if text == correct_text:
                q['correct_label'] = label
                break

    return{
        "data":{
            "subject":subj,
            "count":count,
            "duration":dur_time,
            "seed":seed
        },
        "questions": final_shuffle
    } 


def results(user_answers, exam_data, userTime):

    correct_count = 0
    uncorrect_ques = []

    for i, q in enumerate(exam_data['questions']):

        if i < len(user_answers):                                                                  
            user_choice = user_answers[i]                                     #Lấy nhãn đáp án người dùng chọn (mặc định là None nếu họ bỏ trống)
        else: 
            user_choice=None 
      
        correct_label = q['correct_label']
        
        if user_choice == correct_label:                                      #So sánh nhãn người dùng chọn với đáp án đúng
            correct_count += 1
        else:
            uncorrect_ques.append({                                           #Ghi lại chi tiết để phân tích lỗi sai
                "question": q['text'],
                "user_choice": user_choice,
                "correct_label": correct_label,
                "correct_text": q['answers'].get(correct_label, "N/A")
            })
            
    total = len(exam_data['questions'])

    if total > 0:
        score = (correct_count / total) * 10  
    else:       
        score=0
    
    return {
        "score": round(score, 2),
        "correct_count": correct_count,
        "total": total,
        "userTime": userTime,
        "uncorrect": uncorrect_ques
    }