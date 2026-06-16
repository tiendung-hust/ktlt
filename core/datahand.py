import json
import os

QUESTIONS_FILE = 'data/questions.json'
RESULTS_FILE = 'data/results.json'

def loadData(filepath):
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Nếu file tồn tại nhưng bị lỗi cú pháp JSON thì trả về mảng rỗng
        return []

def saveData(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def updateData(filepath, new_item):
    data = loadData(filepath)
    
    # Logic tự động tăng ID nếu là file ngân hàng câu hỏi
    if "questions" in filepath:
        if len(data) == 0:
            new_item["id"] = 1
        else:
            # Tìm ID lớn nhất trong mảng hiện tại và cộng thêm 1
            max_id = max([item.get("id", 0) for item in data])
            new_item["id"] = max_id + 1
        
    data.append(new_item)
    saveData(filepath, data)
    return True

def updateComment(filepath, exam_id, comment):
    data = loadData(filepath)
    is_updated = False
    
    # Duyệt qua mảng kết quả để tìm đúng bài thi
    for item in data:
        if item.get("exam_id") == exam_id:
            item["status"] = "graded"  # Cập nhật trạng thái thành 'đã chấm'
            is_updated = True
            break  # nếu tìm thấy thì thoát vòng lặp
            
    # Nếu tìm thấy và sửa thành công thì mới lưu vào ổ cứng
    if is_updated:
        saveData(filepath, data)
        return True
        
    return False # Trả về False nếu không tìm thấy exam_id