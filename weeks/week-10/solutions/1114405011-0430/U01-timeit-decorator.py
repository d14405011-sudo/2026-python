# U01. 計時裝飾器實作與資料格式速度比較（6.1 / 6.2 / 6.3）
# 從「重複的計時程式碼」出發，引入裝飾器，再做格式實驗
#
# 本練習學習重點：
#   6.1  裝飾器 (Decorator) 的基本概念與語法
#   6.2  functools.wraps 保留原始函式的 metadata
#   6.3  比較 CSV / JSON / XML 三種文字資料格式的讀取效能

import csv                              # Python 標準函式庫：解析 CSV 格式
import json                             # Python 標準函式庫：解析 JSON 格式
import time                             # Python 標準函式庫：提供高精度計時功能
import io                               # Python 標準函式庫：在記憶體中模擬檔案物件
import xml.etree.ElementTree as ET      # Python 標準函式庫：解析 XML 格式（使用 C 語言加速版本）
import functools                        # Python 標準函式庫：提供 wraps 等高階函式工具

# ═══════════════════════════════════════════════════════════
# Part 1｜問題：每個函式都要手動計時 → 大量重複
# ═══════════════════════════════════════════════════════════
# 三個簡單的「讀取函式」，各自把不同格式的字串解析成 Python list

def read_csv_raw(data: str) -> list:
    # csv.DictReader 把字串當成 CSV 檔案讀取，每一列解析成一個 dict
    # io.StringIO 的作用是把記憶體字串包裝成「類檔案物件」，讓 DictReader 以為在讀一個真實的檔
    return list(csv.DictReader(io.StringIO(data)))

def read_json_raw(data: str) -> list:
    # json.loads 直接把 JSON 格式字串反序列化成 Python 物件 (此處為 list of dict)
    return json.loads(data)

def read_xml_raw(data: str) -> list:
    # ET.fromstring 解析 XML 字串，傳回根節點 (root element)
    root = ET.fromstring(data)
    # 找出所有 <row> 子標籤，並取出每個標籤的屬性 (.attrib) 字典收集成串列
    return [r.attrib for r in root.findall("row")]

# 沒有裝飾器：每次都要複製貼上計時程式碼 ↓
# start = time.perf_counter()
# result = read_csv_raw(data)
# print(f"read_csv_raw 耗時 {time.perf_counter() - start:.6f}s")
#
# start = time.perf_counter()
# result = read_json_raw(data)
# print(f"read_json_raw 耗時 {time.perf_counter() - start:.6f}s")
# ... 每加一個函式就多寫三行，且容易忘記移除

# ═══════════════════════════════════════════════════════════
# Part 2｜解法：裝飾器把計時邏輯包起來，一次定義，到處復用
# ═══════════════════════════════════════════════════════════
# 裝飾器本質上是一個「接受函式、回傳函式」的高階函式
# 透過 @timeit 語法，Python 會自動執行 func = timeit(func)

def timeit(func):
    """基礎版：在呼叫前後計時，印出耗時"""
    # wrapper 是裝飾器在內部定義的「替代函式」，它包住了原始函式的呼叫
    def wrapper(*args, **kwargs):
        # time.perf_counter() 取得當下「效能計數器」的時間戳，精度比 time.time() 更高
        start = time.perf_counter()
        # 執行被包住的原始函式，並把所有引數（位置引數 *args 和關鍵字引數 **kwargs）原封不動傳遞進去
        result = func(*args, **kwargs)
        # 再次取時間戳，相減即可得到執行耗時
        elapsed = time.perf_counter() - start
        # 以「左對齊 20 字元寬」格式印出函式名稱與耗時 (精確到微秒：6 位小數)
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        # 把原始函式的回傳值原樣傳回，確保不破壞呼叫端的行為
        return result
    return wrapper  # 回傳包裝好的新函式

# ── 問題展示：wrapper 會蓋掉原函式的重要識別資訊 ───────────
# 直接回傳 wrapper 而沒有 functools.wraps 的話，會導致：
#   wrapped.__name__  →  "wrapper"（而非原本的 "demo"）
#   wrapped.__doc__   →  None（說明文件遺失）
def demo():
    """這是 demo 的說明文字"""
    pass

wrapped = timeit(demo)
print("未加 wraps 前：", wrapped.__name__)   # wrapper（錯誤！）

# ── Part 3｜functools.wraps：保留原函式的 metadata ──────────
# 重新定義 timeit，這次加上 @functools.wraps(func) 裝飾內層的 wrapper

def timeit(func):
    @functools.wraps(func)          # 把 func 的 __name__ / __doc__ / __module__ 等屬性「複製」到 wrapper 上
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        return result
    return wrapper

wrapped = timeit(demo)
print("加 wraps 後：  ", wrapped.__name__)   # demo（正確）
print()

# ═══════════════════════════════════════════════════════════
# Part 4｜實驗：相同資料，CSV vs JSON vs XML 速度比較
# ═══════════════════════════════════════════════════════════

# ── 產生測試資料（1000 筆學生記錄）────────────────────────
N = 1000  # 定義測試資料筆數

# 在記憶體中動態產生 CSV 格式字串
csv_buf = io.StringIO()  # 建立一個記憶體中的「類檔案物件」作為 CSV 寫入目標
writer = csv.DictWriter(csv_buf, fieldnames=["id", "name", "score"])
writer.writeheader()     # 寫入欄位標頭行 (id, name, score)
for i in range(N):
    # 用格式化字串 f"Student{i:04d}" 產生固定 4 位數字補零的學生編號 (e.g. Student0001)
    # score 以 60 + i % 40 讓成績在 60~99 之間循環分布
    writer.writerow({"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40})
CSV_DATA = csv_buf.getvalue()  # 取出整個 CSV 字串

# 在記憶體中動態產生 JSON 格式字串
JSON_DATA = json.dumps([                 # json.dumps 將 Python list of dict 序列化成 JSON 字串
    {"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40}
    for i in range(N)                    # 使用串列生成式 (list comprehension) 一次建立所有資料列
])

# 在記憶體中動態產生 XML 格式字串
xml_rows = "".join(                      # 用字串串接把每列的 XML 標籤組合在一起
    f'<row id="{i}" name="Student{i:04d}" score="{60 + i % 40}"/>'
    for i in range(N)                    # 生成器運算式 (generator expression) 節省記憶體
)
XML_DATA = f"<data>{xml_rows}</data>"    # 包上最外層的根標籤 <data>

# ── 帶回傳耗時的計時包裝（靜默版：不印出，只回傳結果和時間）─
# 與前面的 timeit 不同，這版本以 tuple (result, elapsed) 形式回傳，方便後續自行處理時間數值
def timeit_silent(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        # 回傳兩個值：原函式執行結果 + 耗費時間（秒）
        return result, time.perf_counter() - start
    return wrapper

# 分別用 timeit_silent 把三個原始讀取函式包裝成「可回傳耗時」的版本
_csv  = timeit_silent(read_csv_raw)
_json = timeit_silent(read_json_raw)
_xml  = timeit_silent(read_xml_raw)

# ── 執行比較（重複 5 次取平均，排除冷啟動影響）────────────
# 第一次執行通常因 JIT 暖機、快取未建立等因素較慢
# 重複多次取平均可以得到更穩定、具參考價值的數據

RUNS = 5
times = {"CSV": 0.0, "JSON": 0.0, "XML": 0.0}  # 初始化各格式的累計耗時為 0

for _ in range(RUNS):
    # 使用「忽略引數」的慣用底線變數名 _ 代表我們不需要迴圈計數器的值
    _, t = _csv(CSV_DATA);   times["CSV"]  += t  # 執行並累加 CSV 耗時
    _, t = _json(JSON_DATA); times["JSON"] += t  # 執行並累加 JSON 耗時
    _, t = _xml(XML_DATA);   times["XML"]  += t  # 執行並累加 XML 耗時

print(f"=== 讀取 {N} 筆資料，重複 {RUNS} 次平均 ===\n")
print(f"{'格式':<6} {'平均耗時':>12}  {'相對 JSON':>10}")
base = times["JSON"] / RUNS  # 以 JSON 的平均耗時作為比較基準 (倍數計算分母)
for fmt, total in times.items():
    avg = total / RUNS  # 計算此格式的平均耗時（總耗時 ÷ 執行次數）
    print(f"  {fmt:<6} {avg:.6f}s   {avg/base:>8.2f}x")  # 印出平均耗時與相對 JSON 的速度倍數

# ═══════════════════════════════════════════════════════════
# 觀察重點
# ═══════════════════════════════════════════════════════════
# 1. JSON 通常最快（原生 C 實作的解析器）
# 2. XML  通常最慢（文字解析開銷大，屬性字串轉換）
# 3. CSV  介於中間（簡單格式，但每欄都是字串需自行轉型）
#
# 裝飾器帶來的好處：
# - 計時邏輯只寫一次，不汙染原函式
# - 要移除計時只需拿掉 @timeit，函式本身不需修改
# - functools.wraps 確保 debug / help() 時能看到正確名稱
