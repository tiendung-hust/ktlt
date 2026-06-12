# KẾ HOẠCH DỰ ÁN
## Hệ thống thi trắc nghiệm

---

**Nhóm 12:** Dương Tiến Dũng và Phan Tiến Hưng 
\ **Trường:** Đại học Bách Khoa Hà Nội

# Mục lục
## Tổng quan dự án
## Yêu cầu nộp bài
## Phân công nhóm 
## Phân tích bài toán
## Thiết kế hệ thống 
## Thuật Toán
## Kiểm thử và đo hiệu năng
## Cấu trúc báo cáo
---
# Tổng quan dự án:
**Ngôn ngữ lựa chọn:** Python.
### 1.1 Mô tả bài toán: 

Hệ thống hỗ trợ quản lý ngân hàng câu hỏi, tự động tạo đề thi theo ma trận độ khó và chấm điểm, phân tích lỗi sai chi tiết. Giải pháp tối ưu cho việc ôn luyện và kiểm tra kiến thức trắc nghiệm.

### 1.2 Mục tiêu:
 
* Tự động hóa quy trình thi: Xây dựng một hệ thống khép kín từ việc tạo đề thi tự động đến chấm điểm, giúp tiết kiệm thời gian và giảm thiểu sai sót so với việc chấm thủ công.

* Đảm bảo tính công bằng: Thiết kế cơ chế xáo trộn đáp án thông minh và ngẫu nhiên hóa thứ tự câu hỏi, đảm bảo mỗi người thi có một đề thi duy nhất, hạn chế tối đa gian lận.

* Quản lý khoa học: Tổ chức ngân hàng câu hỏi theo ma trận độ khó (Dễ, Trung bình, Khó) và chủ đề, cho phép người dùng tùy chỉnh cấu trúc đề thi linh hoạt theo nhu cầu ôn luyện.

* Phản hồi tức thì: Cung cấp kết quả chấm điểm ngay lập tức kèm theo bảng phân tích lỗi sai, giúp người dùng nhận diện lỗ hổng kiến thức và cải thiện hiệu quả học tập.

---

# Yêu cầu nộp bài

## 1. Yêu cầu kỹ thuật cốt lõi
- **Tự cài đặt cấu trúc dữ liệu:** Không được sử dụng các cấu trúc dữ liệu nâng cao hoặc thư viện có sẵn (ví dụ: `list`, `hash`, `queue`, thư viện ma trận, thư viện số lớn, các thư viện sắp xếp/tìm kiếm tích hợp sẵn).
- **Yêu cầu:** Phải tự cài đặt thủ công toàn bộ các cấu trúc dữ liệu và thuật toán được sử dụng trong chương trình.

## 2. Yêu cầu chung của chương trình
- **Menu điều khiển:** Người dùng chọn tác vụ từ menu đơn giản để thực hiện các chức năng cho đến khi chọn kết thúc chương trình.
- **Lưu trữ dữ liệu:** Dữ liệu vào/ra phải được lưu trữ trong file văn bản (định dạng gợi ý: JSON, XML, hoặc lưu theo dòng). Cho phép nhập liệu từ bàn phím và xuất dữ liệu xuống file.
- **Kỹ thuật lập trình:** Vận dụng đúng các kỹ thuật thiết kế, lập trình và kiểm thử phần mềm.

## 3. Yêu cầu kết quả nộp bài
Kết quả nộp bài bao gồm 2 thành phần chính:

### (1) File Báo cáo (định dạng Word)
Báo cáo cần tuân thủ thể thức của Đại học và bao gồm các thông tin:
- **a.** Thông tin người thực hiện, phân công nhiệm vụ (nếu là nhóm).
- **b.** Mô tả tổng thể các chức năng, thiết kế/tổ chức chương trình và cấu trúc file dữ liệu.
- **c.** Các tình huống kiểm thử (Test cases) và kết quả thực hiện (kèm hình ảnh minh họa).
- **d.** Tổng kết các kỹ thuật đã vận dụng.
- **e.** Phụ lục: Mã nguồn hàm `main` và mô tả các hàm xử lý nghiệp vụ chính.

### (2) File nén (.zip hoặc .rar)
Chứa toàn bộ mã nguồn của chương trình:
- **a.** Thư mục chứa các file mã nguồn.
- **b.** Các file dữ liệu phục vụ chương trình.

*Lưu ý: Cần chuẩn bị báo cáo in để nộp và ký danh sách thi theo quy định.*

---

# Phân công nhóm 

### 2.1 Thành viên 1: Logic lõi 
Trọng tâm là xử lý mảng và từ điển bằng code tay:
- **`core/algorithms.py`**:
    - `randomLCG`: Class sinh số ngẫu nhiên thủ công (Linear Congruential Generator).
    - `shuffle(arr)`: Thuật toán Fisher-Yates để xáo trộn câu hỏi và đáp án.
    - `bubbleSort(arr, key)`: Thuật toán sắp xếp danh sách thi giảm dần theo điểm số (`score`).
- **`core/exam.py`**:
    - `exam`: Lọc câu hỏi theo môn/độ khó, bốc câu hỏi ngẫu nhiên và xáo trộn đáp án.
    - `results`: Chấm điểm tự động và trả về dữ liệu đối chiếu lỗi sai cho Dashboard.

### 2.2 Thành viên 2: Giao diện & Dữ liệu 
Trọng tâm là xây dựng GUI và quản lý trạng thái:
- **`gui/datahand.py`**: 
    - `loaddata` / `savedata`: Xử lý nạp và lưu trữ file dữ liệu.
    - `save_result()`: Ghi lịch sử thi vào `results.json` sau mỗi lần nộp bài.
- **`gui/app.py`**: 
    - **Cấu trúc GUI**: Sử dụng kỹ thuật ẩn/hiện `Frame` của tkinter gồm 4 màn hình: Start Screen, Exam Screen (với `Canvas` + `Scrollbar`), Dashboard (Result Screen), và Leaderboard (dùng `Treeview`).
    - **Thời gian**: Sử dụng `root.after(1000, update_timer)` để đếm ngược và tự động nộp bài khi hết giờ.

---

# Phân tích bài toán 

## Đầu vào (Input) và Đầu ra (Output)

### Đầu vào:
- **Ngân hàng câu hỏi:** File `questions.json` chứa danh sách câu hỏi, bao gồm: nội dung, 4 đáp án, đáp án đúng và phân loại độ khó (Dễ/Vừa/Khó).
- **Cấu hình kỳ thi:** Người dùng chọn Môn học, Thời gian làm bài và số lượng câu hỏi thông qua giao diện.
- **Bài làm của thí sinh:** Danh sách đáp án người dùng chọn trong quá trình làm bài.

### Đầu ra:
- **Đề thi:** Một danh sách câu hỏi đã được xáo trộn thứ tự và xáo trộn đáp án.
- **Kết quả chi tiết:** Tổng điểm (thang 10), danh sách câu trả lời đúng/sai và thời gian hoàn thành.
- **Phân tích:** Bảng đối chiếu lỗi sai (hiển thị câu trả lời của người dùng so với đáp án đúng).
- **Lịch sử thi:** Lưu trữ kết quả vào `results.json` để phục vụ chức năng bảng xếp hạng.


## Cấu trúc dữ liệu

| Cấu trúc | Mục đích | Lý do chọn |
| :--- | :--- | :--- |
| **Dictionary/JSON** | Lưu trữ ngân hàng câu hỏi | Truy xuất nhanh theo khóa, cấu trúc linh hoạt |
| **List (Tự cài đặt)** | Quản lý danh sách câu hỏi trong đề | Lưu trữ tuần tự, dễ dàng duyệt và thao tác |
| **Fisher-Yates (Shuffle)** | Xáo trộn thứ tự câu hỏi và đáp án | Đảm bảo tính ngẫu nhiên $O(n)$ không dùng thư viện |
| **Bubble Sort** | Sắp xếp lịch sử thi (Bảng xếp hạng) | Cài đặt thủ công, trực quan trong quy mô dữ liệu nhỏ |
| **Dictionary** | Lưu trữ kết quả thi (`results.json`) | Dễ dàng ánh xạ thông tin người dùng với điểm số |

---

# Thiết kế hệ thống 
### Thiết kế Diagram
```text
+-----------------------+    +-----------------------+
|      Question         |    |      ExamEngine       |
+-----------------------+    +-----------------------+
| - id: int             |    | - bank: list          |
| - diff_matrix: dict   |    | - diff: str           |
| - subject: str        |    | + exam()              |
| - correct: str        |    | + results()           |
+-----------------------+    +-----------------------+
           
           
+-----------------------+    +-----------------------+
|      Algorithms       |    |      DataHandler      |
+-----------------------+    +-----------------------+
| + randomLCG(seed)     |    | + loadData()          |
| + shuffle(arr)        |    | + saveData()          |
| + bubbleSort(arr, key)|    | + saveResult()        |
+-----------------------+    +-----------------------+
           
           
+-----------------------+
|        AppGUI         |
+-----------------------+
| - current_frame       |
| + showMenu()          |
| + startTimer()        |
| + updateDisplay()     |
+-----------------------+
```
### Format dữ liệu(JSON)
```text
{
    "id": 1,
    "subject": "Toan",
    "difficulty": "Easy",
    "text": "Tính 12 + 8.",
    "answers": {
      "A": "20",
      "B": "21",
      "C": "19",
      "D": "22"
    },
    "correct_label": "A"
  }
```
---

# Thuật toán

### Peseudocode
```text
CLASS randomLCG:
    FUNCTION initialize(seed):
        state = seed, a = 1664525, c = 1013904223, m = 2^32
    FUNCTION next(low, high):
        state = (a * state + c) MOD m
        RETURN low + (state MOD (high - low))

FUNCTION shuffle(arr, seed):
    rdm = NEW randomLCG(seed)
    shuffled = COPY(arr)
    FOR i FROM LENGTH(shuffled) - 1 DOWN TO 1:
        j = rdm.next(0, i + 1)
        SWAP shuffled[i] WITH shuffled[j]
    RETURN shuffled

FUNCTION bubbleSort(arr, key):
    sorted_arr = COPY(arr)
    FOR i FROM 0 TO LENGTH(sorted_arr) - 1:
        FOR j FROM 0 TO LENGTH(sorted_arr) - i - 2:
            IF key(sorted_arr[j]) < key(sorted_arr[j+1]):
                SWAP sorted_arr[j] WITH sorted_arr[j+1]
    RETURN sorted_arr

FUNCTION exam(dur_time, bank, count, subj, diff_matrix):
    seed = GET_CURRENT_TIME_MILLISECONDS()
    ex_ques = []
    
    // 1. Lọc và chọn câu hỏi theo tỉ lệ độ khó
    FOR EACH (difficulty, ratio) IN diff_matrix:
        num_to_get = INTEGER(count * ratio)
        filtered = FILTER bank WHERE subject == subj AND difficulty == difficulty
        shuffled_filtered = CALL shuffle(filtered, seed)
        APPEND first num_to_get elements OF shuffled_filtered TO ex_ques
    
    // 2. Xáo trộn thứ tự đề thi cuối cùng
    final_exam = CALL shuffle(ex_ques, seed)
    
    // 3. Xáo trộn vị trí đáp án cho từng câu
    FOR EACH question IN final_exam:
        correct_text = question.answers[question.correct_label]
        shuffled_answers = CALL shuffle(LIST(question.answers.values()), seed)
        
        NEW new_answers_map = {}
        FOR i FROM 0 TO LENGTH(question.answers):
            new_answers_map[original_labels[i]] = shuffled_answers[i]
        
        question.answers = new_answers_map
        // Cập nhật lại nhãn đáp án đúng mới
        question.correct_label = FIND_KEY(question.answers, correct_text)
        
    RETURN {data: config, questions: final_exam}

FUNCTION results(user_answers, exam_data, userTime):
    correct_count = 0
    uncorrect_list = []
    
    FOR i FROM 0 TO LENGTH(exam_data.questions) - 1:
        user_choice = (i < LENGTH(user_answers)) ? user_answers[i] : NULL
        correct_label = exam_data.questions[i].correct_label
        
        IF user_choice == correct_label:
            correct_count = correct_count + 1
        ELSE:
            APPEND {question, user_choice, correct_label} TO uncorrect_list
            
    score = (correct_count / LENGTH(exam_data.questions)) * 10
    RETURN {score, correct_count, total, userTime, uncorrect_list}
```
###  Phân tích độ phức tạp thuật toán

| Thuật toán | Thời gian (Time) | Không gian (Space) |
| :--- | :--- | :--- |
| **Fisher-Yates Shuffle** | $O(N)$ | $O(N)$ |
| **Bubble Sort** | $O(N^2)$ | $O(N)$ |
| **`generate_exam`** | $O(N + M)$ | $O(M)$ |
*(Với $N$: tổng số câu hỏi trong ngân hàng, $M$: số câu hỏi trong một đề thi)*

---

# Kiểm thử và đo hiệu năng


---

# Cấu trúc báo cáo