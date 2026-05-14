# R01. CSV 基礎讀寫（6.1）
# csv.reader / csv.writer / csv.DictReader / csv.DictWriter
#
# CSV（Comma-Separated Values）是一種以逗號分隔欄位的純文字格式，
# 廣泛用於試算表、資料庫的資料交換。
# Python 內建的 csv 模組提供了讀寫 CSV 的標準工具。

import csv   # 內建 CSV 讀寫模組
import io    # 提供 StringIO，讓字串可當作檔案物件操作

# ── 範例資料（模擬 CSV 字串）────────────────────────────
# 使用多行字串模擬一個 CSV 檔案的內容，包含：
#   Symbol（股票代號）、Price（股價）、Date（日期）、
#   Time（時間）、Change（漲跌）、Volume（成交量）
raw = """Symbol,Price,Date,Time,Change,Volume
AA,39.48,6/11/2007,9:36am,-0.18,181800
AIG,71.38,6/11/2007,9:36am,-0.15,195500
AXP,62.58,6/11/2007,9:36am,-0.46,935000
"""

# ── 6.1 csv.reader：逐列讀取，每列是 list ───────────────
# csv.reader 會將每一列解析為 Python list，
# 欄位之間以逗號分隔（預設），適合欄位位置固定的情況。
print("=== csv.reader ===")
f = io.StringIO(raw)        # 將字串包裝成類檔案物件，讓 csv.reader 可以讀取
reader = csv.reader(f)      # 建立 reader 物件，讀取 f 的每一列
headers = next(reader)      # 呼叫 next() 取出第一列作為欄位標頭（跳過，不當資料處理）
print("標頭：", headers)    # 印出欄位名稱清單
for row in reader:          # 逐列讀取剩餘資料列
    print(row)              # 每列印出一個 list，例如 ['AA', '39.48', ...]

# ── 6.1 csv.DictReader：每列自動對應成 dict ──────────────
# csv.DictReader 以第一列作為欄位名稱（key），
# 將後續每列自動包裝成 dict，可用欄位名稱存取值，比 index 更直觀。
print("\n=== csv.DictReader ===")
f = io.StringIO(raw)        # 重新建立 StringIO（因為前面已讀到底）
for row in csv.DictReader(f):
    # row 是一個 dict，例如 {'Symbol': 'AA', 'Price': '39.48', ...}
    # :5s  → 靠左對齊，共 5 個字元寬（字串格式）
    # :>6s → 靠右對齊，共 6 個字元寬
    print(f"{row['Symbol']:5s}  價格={row['Price']:>6s}  漲跌={row['Change']}")

# ── 6.1 csv.writer：寫出 CSV ─────────────────────────────
# csv.writer 將 Python list 寫成 CSV 格式的列，
# 自動處理逗號、換行、特殊字元的跳脫（escape）。
print("\n=== csv.writer ===")
output = io.StringIO()              # 建立一個可寫入的字串緩衝區
writer = csv.writer(output)         # 建立 writer 物件，寫入 output
writer.writerow(["Symbol", "Price", "Change"])  # 寫入標頭列
writer.writerow(["AA", 39.48, -0.18])           # 寫入第一筆資料
writer.writerow(["AIG", 71.38, -0.15])          # 寫入第二筆資料
print(output.getvalue())            # 取得緩衝區內所有已寫入的字串並印出

# ── 6.1 csv.DictWriter：以 dict 寫出 CSV ─────────────────
# csv.DictWriter 以欄位名稱對應的 dict 寫入 CSV，
# 需先指定 fieldnames（欄位順序），並呼叫 writeheader() 寫入標頭列。
print("=== csv.DictWriter ===")
output = io.StringIO()                          # 建立新的字串緩衝區
fieldnames = ["Symbol", "Price", "Change"]      # 定義欄位名稱與順序
writer = csv.DictWriter(output, fieldnames=fieldnames)  # 建立 DictWriter 物件
writer.writeheader()                            # 自動寫入欄位名稱作為第一列（標頭）
writer.writerow({"Symbol": "AA",  "Price": 39.48, "Change": -0.18})  # 用 dict 寫入資料
writer.writerow({"Symbol": "AIG", "Price": 71.38, "Change": -0.15})  # 用 dict 寫入資料
print(output.getvalue())            # 印出最終的 CSV 字串內容

# ── 常用參數 ─────────────────────────────────────────────
# csv.reader / csv.writer 支援以下常用參數來調整解析行為：
#
# delimiter='\t'        → 改用 Tab 分隔欄位，即 TSV（Tab-Separated Values）格式
# quotechar='"'         → 指定用於包裹含特殊字元欄位的引號字元（預設為雙引號）
# quoting=csv.QUOTE_ALL → 強制每個欄位都加上引號（預設只在必要時才加）
#
# 其他常用 quoting 選項：
#   csv.QUOTE_MINIMAL   → 只在含特殊字元時才加引號（預設值）
#   csv.QUOTE_NONNUMERIC → 所有非數字欄位都加引號
#   csv.QUOTE_NONE      → 不加任何引號（需同時指定 escapechar）
