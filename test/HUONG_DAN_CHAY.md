# Mã nguồn Chương 8 — Kiểm thử và Đo đạc hiệu năng

## LƯU Ý QUAN TRỌNG TRƯỚC KHI CHẠY: vị trí lưu file

Các lệnh `python ten_file.py` chỉ tìm file trong ĐÚNG thư mục mà terminal
đang đứng (thư mục hiện hành). Nếu bạn lưu các file .py này vào một thư
mục con (ví dụ thư mục `test/`) nhưng terminal lại đang đứng ở thư mục
gốc của project, lệnh sẽ báo lỗi "No such file or directory" dù file
vẫn tồn tại.

Cách kiểm tra terminal đang đứng ở đâu: gõ `dir` (Windows) hoặc `ls`
(macOS/Linux) — nếu thấy đúng tên các file .py liệt kê ở dưới thì bạn
đang đứng đúng chỗ, chạy lệnh `python ten_file.py` bình thường.

Nếu file nằm trong một thư mục con (ví dụ `test/benchmark_chuong8.py`),
có 2 cách chạy:

```
:: Cách 1 - di chuyển vào đúng thư mục con trước
cd test
python benchmark_chuong8.py
python plot_chuong8.py

:: Cách 2 - đứng ở thư mục gốc, chỉ rõ đường dẫn tới thư mục con
python test/benchmark_chuong8.py
python test/plot_chuong8.py
```

Khuyến nghị: gom toàn bộ 4 file (testcase.py, benchmark_chuong8.py,
plot_chuong8.py, HUONG_DAN_CHAY.md) vào CHUNG một thư mục, rồi `cd`
vào đúng thư mục đó trước khi chạy bất kỳ lệnh python nào bên dưới —
sẽ tránh được toàn bộ lỗi đường dẫn.

## 1. Chạy lại Test case (testcase.py)

File `testcase.py` này CHÍNH LÀ file test gốc của bạn (không thay đổi).
Để chạy, copy file này vào thư mục gốc của project (ngang hàng với main.py),
rồi chạy:

```
python testcase.py
```

Trên máy cá nhân (Windows / macOS / Linux có desktop bình thường) — TỨC LÀ
 KHI CHẠY TRÊN VS CODE — chỉ cần lệnh trên là đủ, KHÔNG CẦN cài thêm gì khác. 
 Tkinter đã có sẵn màn hình thật để vẽ (dù testcase.py có ẩn cửa sổ bằng root.withdraw()).

Xvfb (X Virtual Framebuffer) CHỈ cần khi chạy trên môi trường KHÔNG có
màn hình đồ hoạ, ví dụ:
- Server Linux không có desktop
- WSL chưa cấu hình GUI
- Môi trường CI/CD (GitHub Actions, GitLab CI...)
- Sandbox của Claude khi nhóm thử nghiệm

Trong các trường hợp đó mới cần (chỉ trên Linux):
```
sudo apt install xvfb
xvfb-run -a python3 testcase.py
```

Tóm lại: nếu chạy trên VS Code ở máy cá nhân có màn hình, BỎ QUA
phần Xvfb này hoàn toàn — chỉ chạy `python testcase.py` là xong.

## 2. Đo hiệu năng trước/sau tối ưu (benchmark_chuong8.py)

File này KHÔNG cần import project gốc — nó tự định nghĩa lại 2 phiên bản
bubble_sort (trước và sau khi thêm cờ swapped) ngay bên trong, nên có thể
chạy độc lập ở bất kỳ đâu có Python 3, không cần cấu trúc thư mục project:

```
python benchmark_chuong8.py
```

Kết quả in ra console và xuất file `benchmark_chuong8_results.csv`
chứa toàn bộ số liệu thô (đã có sẵn 1 bản mẫu trong thư mục này,
chạy lại sẽ ghi đè bằng số liệu đo trên máy của bạn).

Thời gian chạy: khoảng 1-2 phút (do N=10.000 ở kịch bản ngẫu nhiên
mất vài chục giây cho mỗi phiên bản thuật toán).

## 3. Vẽ biểu đồ (plot_chuong8.py)

Yêu cầu cài matplotlib trước:

```
pip install matplotlib
```

Sau đó chạy (PHẢI chạy benchmark_chuong8.py trước để có file CSV):

```
python plot_chuong8.py
```

Sẽ xuất ra 4 file ảnh PNG trong cùng thư mục:
- chart_scenario_random.png   — Hình 14 trong báo cáo
- chart_scenario_sorted.png   — Hình 15 trong báo cáo
- chart_tonghop_4duong.png    — Hình 12 trong báo cáo
- chart_he_so_cai_thien.png   — Hình 13 trong báo cáo

## Lưu ý

Số liệu trong file benchmark_chuong8_results.csv đính kèm là số liệu
nhóm đã đo thực tế (dùng trong báo cáo). Nếu chạy lại trên máy cá nhân, 
số liệu tuyệt đối (ms) sẽ khác đôi chút tuỳ cấu hình máy, nhưng XU HƯỚNG
 và TỈ LỆ cải thiện sẽ tương đồng.