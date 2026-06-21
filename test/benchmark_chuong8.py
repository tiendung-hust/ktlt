"""
============================================================================
SCRIPT ĐO ĐẠC HIỆU NĂNG THUẬT TOÁN BUBBLE SORT — TRƯỚC VÀ SAU TỐI ƯU
============================================================================
File này so sánh hiệu năng giữa 2 phiên bản bubble_sort():
  - Phiên bản TRƯỚC tối ưu: không có cờ swapped, luôn chạy đủ n lượt
  - Phiên bản SAU tối ưu: có cờ swapped, dừng sớm khi mảng đã sắp xếp xong

Cả 2 phiên bản được đo trên 2 kịch bản dữ liệu khác nhau:
  - Kịch bản A "Ngẫu nhiên": dữ liệu xáo trộn hoàn toàn (mô phỏng điểm thi
    thực tế của nhiều thí sinh khác nhau — gần với trường hợp trung bình)
  - Kịch bản B "Đã sắp sẵn": dữ liệu đã ở đúng thứ tự giảm dần từ trước
    (mô phỏng trường hợp tốt nhất — best case)

CÁCH CHẠY:
  python3 benchmark_chuong8.py

KẾT QUẢ:
  - In bảng số liệu ra màn hình
  - Xuất file benchmark_chuong8_results.csv chứa toàn bộ số liệu thô
============================================================================
"""

import time
import random
import csv
import statistics
import os

# ----- Cấu hình đo đạc -----
SIZES = [100, 500, 1000, 5000, 10000]
REPEAT = 10           # số lần lặp lại mỗi kích thước để lấy trung bình
REPEAT_LARGE = 3      # số lần lặp riêng cho N=10000 ở kịch bản ngẫu nhiên (chạy lâu)
SEED_DATA = 2026      # seed cố định để sinh dữ liệu đầu vào -> tái lập được kết quả


# ============================================================================
# HAI PHIÊN BẢN BUBBLE SORT ĐỂ SO SÁNH
# ============================================================================

def bubble_sort_before(arr, key):
    """Phiên bản TRƯỚC tối ưu — không có cờ swapped, luôn chạy đủ n lượt."""
    n = len(arr)
    sorted_arr = list(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if key(sorted_arr[j]) < key(sorted_arr[j + 1]):
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
    return sorted_arr


def bubble_sort_after(arr, key):
    """Phiên bản SAU tối ưu — có cờ swapped, dừng sớm khi mảng đã sắp xong."""
    n = len(arr)
    sorted_arr = list(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if key(sorted_arr[j]) < key(sorted_arr[j + 1]):
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True
        if not swapped:
            break
    return sorted_arr


# ============================================================================
# SINH DỮ LIỆU CHO 2 KỊCH BẢN
# ============================================================================

def generate_random_data(n, seed):
    """Kịch bản A: dữ liệu điểm số ngẫu nhiên (mô phỏng kết quả thi thực tế)."""
    rng = random.Random(seed)
    return [{"score": rng.uniform(0, 10)} for _ in range(n)]


def generate_sorted_data(n, seed):
    """Kịch bản B: dữ liệu đã sắp xếp sẵn theo đúng thứ tự giảm dần
    (trường hợp tốt nhất - best case)."""
    rng = random.Random(seed)
    scores = sorted([rng.uniform(0, 10) for _ in range(n)], reverse=True)
    return [{"score": s} for s in scores]


# ============================================================================
# HÀM ĐO THỜI GIAN
# ============================================================================

def measure(func, data, repeat):
    """Đo thời gian thực thi func(data, key) lặp lại `repeat` lần,
    trả về (thời gian trung bình ms, độ lệch chuẩn ms)."""
    samples = []
    for _ in range(repeat):
        start = time.perf_counter()
        func(data, key=lambda x: x["score"])
        end = time.perf_counter()
        samples.append((end - start) * 1000)  # đổi sang ms
    mean = statistics.mean(samples)
    stdev = statistics.stdev(samples) if len(samples) > 1 else 0.0
    return mean, stdev


# ============================================================================
# CHẠY TOÀN BỘ BENCHMARK
# ============================================================================

def run_full_benchmark():
    rows = []
    header = f"{'N':>7} | {'Kịch bản':<14} | {'Trước (ms)':>14} | {'Sau (ms)':>14} | {'Cải thiện':>10}"
    print(header)
    print("-" * len(header))

    for n in SIZES:
        repeat_random = REPEAT_LARGE if n >= 10000 else REPEAT
        repeat_sorted = REPEAT  # mảng đã sắp luôn nhanh, không cần giảm repeat

        # ----- Kịch bản A: Ngẫu nhiên -----
        data_random = generate_random_data(n, seed=SEED_DATA)
        before_mean, before_std = measure(bubble_sort_before, data_random, repeat_random)
        after_mean, after_std = measure(bubble_sort_after, data_random, repeat_random)
        improvement = before_mean / after_mean if after_mean > 0 else float('inf')

        rows.append({
            "n": n, "scenario": "random",
            "before_mean_ms": before_mean, "before_std_ms": before_std,
            "after_mean_ms": after_mean, "after_std_ms": after_std,
            "improvement_factor": improvement, "repeat": repeat_random,
        })
        print(f"{n:>7} | {'Ngẫu nhiên':<14} | {before_mean:>11.3f} ms | {after_mean:>11.3f} ms | x{improvement:>8.2f}")

        # ----- Kịch bản B: Đã sắp sẵn -----
        data_sorted = generate_sorted_data(n, seed=SEED_DATA)
        before_mean_s, before_std_s = measure(bubble_sort_before, data_sorted, repeat_sorted)
        after_mean_s, after_std_s = measure(bubble_sort_after, data_sorted, repeat_sorted)
        improvement_s = before_mean_s / after_mean_s if after_mean_s > 0 else float('inf')

        rows.append({
            "n": n, "scenario": "sorted",
            "before_mean_ms": before_mean_s, "before_std_ms": before_std_s,
            "after_mean_ms": after_mean_s, "after_std_ms": after_std_s,
            "improvement_factor": improvement_s, "repeat": repeat_sorted,
        })
        print(f"{n:>7} | {'Đã sắp sẵn':<14} | {before_mean_s:>11.3f} ms | {after_mean_s:>11.3f} ms | x{improvement_s:>8.2f}")
        print()

    # Xuất CSV
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_chuong8_results.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Đã lưu toàn bộ số liệu chi tiết vào: {out_path}")
    return rows


if __name__ == "__main__":
    run_full_benchmark()