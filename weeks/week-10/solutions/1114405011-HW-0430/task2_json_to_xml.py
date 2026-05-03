# task2_json_to_xml.py
# Task 2：讀取 JSON → 轉換為 XML → 輸出
# 學號：1114405011

import functools
import json
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

# ── 路徑設定 ─────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
INPUT_JSON = OUTPUT_DIR / "students.json"
OUTPUT_XML = OUTPUT_DIR / "students.xml"


# ── @timeit 裝飾器（自行實作，不直接複製課堂範例）──────────────
def timeit(func):
    """計時裝飾器：使用 time.perf_counter() 計算函式執行耗時並印出。"""
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
def read_json(filepath: str) -> dict:
    """讀取 JSON 檔案，回傳 dict。"""
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def build_xml_tree(data: dict) -> ET.Element:
    """依據 students.json 的結構建構 XML ElementTree，回傳根節點 <students>。"""
    students_list = data.get("學生清單", [])
    root = ET.Element(
        "students",
        attrib={
            "source": data.get("來源", ""),
            "total": str(len(students_list)),
        },
    )
    for s in students_list:
        ET.SubElement(
            root,
            "student",
            attrib={
                "id":     s.get("學號", ""),
                "dept":   s.get("系所名稱", ""),
                "school": s.get("畢業學校", ""),
                "zip":    s.get("郵遞區號", ""),
            },
        )
    return root


@timeit
def write_xml(data: dict, filepath: str) -> None:
    """將 data dict 轉換為 XML 並寫出檔案（附 XML 宣告）。"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    root = build_xml_tree(data)
    tree = ET.ElementTree(root)
    # indent 讓輸出有縮排（Python 3.9+）
    ET.indent(tree, space="  ")
    with open(filepath, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    print(f"XML 已寫出：{filepath}")


# ── 主程式 ─────────────────────────────────────────────
if __name__ == "__main__":
    # 1. 讀取 Task 1 產生的 JSON
    data = read_json(str(INPUT_JSON))
    print(f"JSON 學生清單筆數：{len(data.get('學生清單', []))}")

    # 2. 轉換並輸出 XML
    write_xml(data, str(OUTPUT_XML))
