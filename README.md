# Hệ thống thi trắc nghiệm

**Bài tập lớn cuối kỳ — Môn Kĩ thuật lập trình (MI3310) — Đại học Bách khoa Hà Nội**

Nhóm 12 — Chủ đề 5: Hệ thống thi trắc nghiệm
Giảng viên hướng dẫn: Vũ Thành Nam

| Họ và tên |
|---|
| Dương Tiến Dũng|
| Phan Tiến Hưng |

---

## Mục lục

* [1. Giới thiệu](#1-giới-thiệu)
* [2. Yêu cầu hệ thống](#2-yêu-cầu-hệ-thống)
* [3. Cài đặt và chạy chương trình](#3-cài-đặt-và-chạy-chương-trình)
* [4. Cấu trúc thư mục dự án](#4-cấu-trúc-thư-mục-dự-án)
* [5. Tài khoản sử dụng](#5-tài-khoản-sử-dụng)
* [6. Các thuật toán tự cài đặt](#6-các-thuật-toán-tự-cài-đặt)
* [7. Cấu trúc dữ liệu lưu trữ](#7-cấu-trúc-dữ-liệu-lưu-trữ)
* [8. Kiểm thử và đo hiệu năng](#8-kiểm-thử-và-đo-hiệu-năng)
* [9. Phân công nhiệm vụ](#9-phân-công-nhiệm-vụ)
* [10. Tài liệu báo cáo](#10-tài-liệu-báo-cáo)

---

## 1. Giới thiệu

Hệ thống thi trắc nghiệm độc lập, chạy trên máy tính cá nhân, không phụ thuộc máy chủ hay
hệ quản trị cơ sở dữ liệu, được xây dựng bằng Python theo kiến trúc lập trình thủ tục và
module hóa, hướng tới quy mô đánh giá nội bộ (lớp học, ôn luyện cá nhân).

Hệ thống cho phép:
- Nạp ngân hàng câu hỏi động từ tệp dữ liệu, tự sinh đề thi theo môn học, số lượng câu và
  ma trận tỉ lệ độ khó (Dễ / Vừa / Khó) do người dùng cấu hình.
- Xáo trộn ngẫu nhiên thứ tự câu hỏi và vị trí đáp án cho mỗi lượt thi.
- Đếm ngược thời gian làm bài, tự động nộp bài khi hết giờ.
- Chấm điểm tức thì, phân tích chi tiết các câu trả lời sai.
- Lưu lịch sử thi, hiển thị bảng xếp hạng theo từng môn học.
- Cho phép giáo viên thêm câu hỏi mới vào ngân hàng và xem chi tiết kết quả/lỗi sai của
  từng ca thi.

**Ràng buộc kỹ thuật cốt lõi của đề tài:** không sử dụng các hàm dựng sẵn của Python cho
xáo trộn và sắp xếp (`random.shuffle()`, `sorted()`, `list.sort()`...). Toàn bộ bộ sinh số
giả ngẫu nhiên, thuật toán xáo trộn và thuật toán sắp xếp đều được tự cài đặt thủ công
trong `core/algorithms.py`.

---

## 2. Yêu cầu hệ thống

- Python **3.8 trở lên** (khuyến nghị 3.10+).
- Thư viện `tkinter` — đi kèm sẵn trong bản cài đặt Python tiêu chuẩn trên Windows/macOS.
  Trên một số bản phân phối Linux cần cài thêm thủ công:
  ```bash
  sudo apt install python3-tk
  ```
- Toàn bộ phần còn lại chỉ dùng thư viện chuẩn của Python (`json`, `os`, `time`, `unittest`)
  — **không cần cài thêm package nào khác** để chạy chương trình chính.
- Để vẽ lại biểu đồ hiệu năng (tùy chọn, không bắt buộc để chạy ứng dụng):
  ```bash
  pip install matplotlib
  ```

---

## 3. Cài đặt và chạy chương trình

```bash
# 1. Clone hoặc giải nén mã nguồn, sau đó di chuyển vào thư mục gốc của dự án
cd ktlt-main

# 2. Chạy chương trình từ thư mục gốc (bắt buộc, vì các đường dẫn dữ liệu
#    trong core/datahand.py là đường dẫn tương đối "data/...")
python main.py
```

Khi khởi động lần đầu, hệ thống tự động:
- Nạp ngân hàng câu hỏi từ `data/questions.json`.
- Khởi tạo `data/results.json` thành mảng rỗng `[]` nếu tệp chưa tồn tại hoặc trống.

> **Lưu ý:** luôn chạy lệnh `python main.py` khi terminal đang đứng tại thư mục gốc của dự
> án (ngang hàng với `main.py`, `core/`, `gui/`, `data/`). Nếu chạy từ một thư mục khác,
> chương trình sẽ không tìm thấy `data/questions.json`.

---

## 4. Cấu trúc thư mục dự án

```
ktlt-main/
├── main.py                      # Điểm khởi chạy duy nhất của chương trình
├── core/                        # Tầng lõi: thuật toán + xử lý nghiệp vụ + I/O dữ liệu
│   ├── algorithms.py            #   randomLCG, shuffle(), bubble_sort()
│   ├── exam.py                  #   exam() — sinh đề thi | results() — chấm điểm
│   └── datahand.py              #   loadData() / saveData() / updateData()
├── gui/                         # Tầng giao diện (Tkinter)
│   ├── app.py                   #   QuizApplication — controller trung tâm, điều hướng Frame
│   ├── login_frame.py           #   Màn hình đăng nhập, phân quyền Admin/User
│   ├── admin_frame.py           #   Giao diện Giáo viên: thêm câu hỏi, xem kết quả thi
│   └── user_frame.py            #   Giao diện Học sinh: cấu hình đề, làm bài, lịch sử, BXH
├── data/
│   ├── questions.json           #   Ngân hàng câu hỏi (450 câu: Toán / Tiếng Anh / Ngữ Văn)
│   └── results.json             #   Lịch sử các ca thi đã diễn ra
├── testcase.py                  # Bộ 12 unit test (unittest), bao phủ core + gui
├── test_report_log.txt          # Log kết quả lần chạy testcase.py gần nhất
└── test/                        # Script đo và vẽ biểu đồ hiệu năng (Chương 8 báo cáo)
    ├── benchmark_chuong8.py      #   Đo Bubble Sort trước/sau khi thêm cờ swapped
    ├── plot_chuong8.py           #   Vẽ 4 biểu đồ từ kết quả benchmark
    ├── benchmark_chuong8_results.csv
    ├── chart_*.png                #   4 biểu đồ đã xuất sẵn, dùng trong báo cáo
    └── HUONG_DAN_CHAY.md          #   Hướng dẫn chạy chi tiết riêng cho thư mục test/
```

**Nguyên tắc kiến trúc:** chiều phụ thuộc một chiều — `gui/` được phép `import` từ `core/`,
nhưng không có chiều ngược lại. `core/algorithms.py` hoàn toàn độc lập, không phụ thuộc bất
kỳ module nghiệp vụ hay giao diện nào.

---

## 5. Tài khoản sử dụng

Hệ thống không có màn hình đăng ký; phân quyền dựa hoàn toàn vào tên đăng nhập gõ ở màn
hình Login (`gui/login_frame.py`):

| Vai trò | Cách đăng nhập | Ghi chú |
|---|---|---|
| **Học sinh** | Gõ bất kỳ tên nào khác `admin`, không cần mật khẩu | Vào thẳng `UserFrame` |
| **Giáo viên (Admin)** | Gõ `admin` ở ô Username → ô mật khẩu tự hiện ra → nhập mật khẩu | Mật khẩu mặc định: `123456` |

---

## 6. Các thuật toán tự cài đặt

Toàn bộ nằm trong `core/algorithms.py`, không sử dụng thư viện `random` hay hàm sắp xếp
dựng sẵn của Python:

### 6.1. Bộ sinh số giả ngẫu nhiên — `class randomLCG`

Cài đặt theo phương pháp đồng dư tuyến tính (Linear Congruential Generator), dùng bộ hệ
số của *Numerical Recipes*: `a = 1664525`, `c = 1013904223`, `m = 2^32`. Bộ hệ số này thỏa
mãn định lý Hull–Dobell, đảm bảo chu kỳ đầy đủ m = 2^32 với mọi giá trị `seed` khởi tạo.

```python
rdm = randomLCG(seed)
rdm.next(low, high)   # trả về số nguyên ngẫu nhiên trong [low, high)
```

### 6.2. Thuật toán xáo trộn — `shuffle(arr, seed)`

Cài đặt thuật toán Fisher-Yates, duyệt mảng từ cuối về đầu, đảm bảo phân bố đều trên mọi
hoán vị có thể. Hàm sao chép mảng đầu vào (`list(arr)`) trước khi xáo trộn để không làm
thay đổi dữ liệu gốc. Độ phức tạp: O(n) thời gian, O(n) không gian.

Trong `core/exam.py`, hàm `exam()` gọi `shuffle()` ba lần với ba mục đích khác nhau: xáo
trộn câu hỏi đã lọc theo từng mức độ khó, xáo trộn lại toàn bộ đề sau khi gộp đủ câu, và
xáo trộn vị trí 4 phương án trả lời của từng câu hỏi.

### 6.3. Thuật toán sắp xếp — `bubble_sort(arr, key)`

Cài đặt Bubble Sort sắp xếp giảm dần, có bổ sung cờ `swapped` để dừng sớm khi mảng đã ở
trạng thái sắp xếp. Tham số `key` là một hàm callback (tương tự đối số `key` của
`sorted()`), cho phép sắp xếp theo bất kỳ tiêu chí nào mà không cần sửa logic bên trong hàm.
Trong hệ thống, hàm này được gọi để sắp xếp bảng xếp hạng theo điểm số:

```python
bubble_sort(results_db, key=lambda x: x.get("score", 0))
```

Độ phức tạp: O(n) ở trường hợp tốt nhất (dữ liệu đã sắp sẵn), O(n²) ở trường hợp trung
bình/xấu nhất. Số liệu đo thực nghiệm chi tiết — xem [mục 8](#8-kiểm-thử-và-đo-hiệu-năng).

---

## 7. Cấu trúc dữ liệu lưu trữ

Hệ thống dùng tệp tin phẳng JSON làm lớp lưu trữ, không dùng hệ quản trị cơ sở dữ liệu.

### `data/questions.json` — Ngân hàng câu hỏi (450 câu)

```json
{
  "id": 1,
  "subject": "Math",
  "difficulty": "Easy",
  "text": "Tinh 12 + 8.",
  "answers": { "A": "20", "B": "21", "C": "19", "D": "22" },
  "correct_label": "A"
}
```

Phân bố: 3 môn học (`Math`, `English`, `Vietnamese`) × 150 câu/môn, mỗi môn gồm 80 câu
Easy, 45 câu Medium, 25 câu Hard.

### `data/results.json` — Lịch sử thi (cơ chế append-only)

```json
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
```

### Module đọc/ghi — `core/datahand.py`

| Hàm | Vai trò |
|---|---|
| `loadData(filepath)` | Nạp tệp JSON lên RAM; trả về `[]` nếu tệp không tồn tại hoặc lỗi cú pháp (`json.JSONDecodeError`), không làm sập chương trình |
| `saveData(filepath, data)` | Ghi đè toàn bộ mảng dữ liệu xuống đĩa (`ensure_ascii=False`, `indent=4`, bảo toàn Unicode tiếng Việt) |
| `updateData(filepath, new_item)` | Nạp dữ liệu cũ → tự sinh `id` tăng dần (nếu là `questions.json`, dùng `max(id) + 1`) → thêm bản ghi mới → ghi đè xuống đĩa |

---

## 8. Kiểm thử và đo hiệu năng

### 8.1. Chạy bộ unit test (`testcase.py`)

```bash
python testcase.py
```

Bộ test gồm **12 kịch bản** (`unittest`), dùng dữ liệu giả lập riêng (không đụng đến
`data/questions.json` và `data/results.json` thật), bao phủ:

- Đăng nhập & phân quyền (4 test)
- Sinh đề thi & cấu hình ma trận độ khó (2 test)
- Làm bài, chấm điểm, đồng hồ đếm ngược (2 test)
- Quản lý dữ liệu: lịch sử thi, thêm câu hỏi, phân tích lỗi sai (4 test)

Kết quả được in ra console đồng thời ghi vào `test_report_log.txt`. Trên môi trường không
có màn hình đồ họa (server, CI/CD, WSL chưa cấu hình GUI), cần chạy qua Xvfb:

```bash
sudo apt install xvfb
xvfb-run -a python3 testcase.py
```

### 8.2. Đo hiệu năng Bubble Sort trước/sau tối ưu

```bash
cd test
python benchmark_chuong8.py     # đo và xuất benchmark_chuong8_results.csv
pip install matplotlib          # nếu chưa cài
python plot_chuong8.py          # vẽ lại 4 biểu đồ PNG từ file CSV
```

Script benchmark tự định nghĩa lại hai phiên bản `bubble_sort` (trước và sau khi thêm cờ
`swapped`), đo trên 5 mốc kích thước dữ liệu (N = 100, 500, 1.000, 5.000, 10.000) ở hai
kịch bản dữ liệu ngẫu nhiên và đã sắp sẵn. Chi tiết phương pháp đo và phân tích kết quả —
xem Chương 8 trong báo cáo, hoặc `test/HUONG_DAN_CHAY.md`.

---

## 9. Phân công nhiệm vụ

| Thành viên | Nhiệm vụ | Mức độ hoàn thành |
|---|---|---|
| **Dương Tiến Dũng** | Lập trình tầng lõi (`core/`: thuật toán, xử lý dữ liệu, logic nghiệp vụ); viết báo cáo; chuẩn bị ngân hàng câu hỏi; viết README; đo đạc hiệu năng | 100% |
| **Phan Tiến Hưng** | Lập trình giao diện (`gui/`); viết test case (`testcase.py`); chuẩn bị nội dung báo cáo phần kiểm thử | 100% |

---

## 10. Tài liệu báo cáo

Báo cáo đầy đủ (phân tích yêu cầu, thiết kế kiến trúc, mô tả thuật toán, kiểm thử và đo
hiệu năng) được trình bày trong file báo cáo nhóm đính kèm, biên soạn bằng LaTeX. Mã nguồn
được quản lý phiên bản tại repository:

```
https://github.com/tiendung-hust/ktlt.git
```
