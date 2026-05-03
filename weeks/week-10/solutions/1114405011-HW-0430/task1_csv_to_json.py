# task1_csv_to_json.py
# Task 1：讀取 CSV → 過濾 → 統計 → 輸出 JSON
# 學號：1114405011

import csv
import functools
import json
import os
import time
from collections import Counter
from pathlib import Path

# ── 路徑設定 ─────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
# 專案根目錄：從 week-10/solutions/1114405011-HW-0430 往上四層 → 2026-python/
PROJECT_ROOT = HERE.parents[3]
# CSV 路徑：2026-python/assets/stu-data/113年新生資料庫.csv
CSV_PATH = PROJECT_ROOT / "assets" / "stu-data" / "113年新生資料庫.csv"
OUTPUT_DIR = HERE / "output"
OUTPUT_JSON = OUTPUT_DIR / "students.json"


# ── @timeit 裝飾器（自行實作，參考課堂 U01-timeit-decorator.py）────────
def timeit(func):
    """計時裝飾器：在呼叫前後以 time.perf_counter() 計時，並印出耗時。"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timeit] {func.__name__} 耗時 {elapsed:.6f}s")
        return result
    return wrapper


# ── 核心函式 ───────────────────────────────────────────
@timeit
def read_csv(filepath: str) -> list[dict]:
    """讀取 CSV 檔案，回傳所有列的 list[dict]。
    注意 113年新生資料庫.csv 使用 UTF-8-BOM 編碼，需指定 encoding='utf-8-sig'。
    """
    with open(filepath, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def filter_by_admission(rows: list[dict], method: str) -> list[dict]:
    """過濾出指定入學方式的列，忽略前後空白。"""
    return [r for r in rows if r.get("入學方式", "").strip() == method.strip()]


def count_by_dept(rows: list[dict]) -> dict:
    """統計各系所名稱的人數，回傳 dict（系所 → 人數）。"""
    counter = Counter(r.get("系所名稱", "").strip() for r in rows)
    return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))


@timeit
def write_json(data: dict, filepath: str) -> None:
    """將 data dict 寫出為 JSON 檔案（確保目錄存在）。"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON 已寫出：{filepath}")


# ── 主程式 ─────────────────────────────────────────────
if __name__ == "__main__":
    # 1. 讀取 CSV
    all_rows = read_csv(str(CSV_PATH))
    print(f"讀取總筆數：{len(all_rows)}")

    # 2. 過濾入學方式 == '聯合登記分發'
    METHOD = "聯合登記分發"
    filtered = filter_by_admission(all_rows, METHOD)
    print(f"篩選「{METHOD}」後筆數：{len(filtered)}")

    # 3. 統計各系所人數
    dept_stats = count_by_dept(filtered)

    # 4. 組合輸出 JSON 結構
    output_data = {
        "來源": "113年新生資料庫",
        "入學方式篩選": METHOD,
        "總人數": len(filtered),
        "系所統計": dept_stats,
        "學生清單": [
            {
                "學號": r.get("學號", "").strip(),
                "系所名稱": r.get("系所名稱", "").strip(),
                "畢業學校": r.get("畢業學校", "").strip(),
                "郵遞區號": r.get("郵遞區號", "").strip(),
            }
            for r in filtered
        ],
    }

    # 5. 輸出 JSON
    write_json(output_data, str(OUTPUT_JSON))
