# R02. JSON 基礎讀寫（6.2）
# json.loads / json.dumps / json.load / json.dump
#
# JSON（JavaScript Object Notation）是一種輕量化的資料交換格式，
# 以純文字表示結構化資料，廣泛用於 Web API、設定檔、資料儲存等場合。
# Python 內建的 json 模組提供了 JSON 與 Python 物件之間互相轉換的工具：
#   dumps / dump  → 序列化（Python 物件 → JSON）
#   loads / load  → 反序列化（JSON → Python 物件）
#   有 's' 的版本處理「字串」；無 's' 的版本處理「檔案」。

import json   # 內建 JSON 處理模組，不需額外安裝

# ── 字串 ↔ Python 物件 ───────────────────────────────────
# 準備一個 Python dict 作為測試資料，包含字串、整數、list 等常見型別
data = {"name": "Alice", "age": 30, "scores": [95, 87, 92]}

# 序列化（Python → JSON 字串）
# json.dumps()：將 Python 物件轉換為 JSON 格式的「字串」（s = string）
# 回傳值是 str 型別，可用於網路傳輸或儲存
s = json.dumps(data)
print(type(s), s)   # 輸出：<class 'str'> {"name": "Alice", "age": 30, "scores": [95, 87, 92]}

# 美化輸出（Pretty Print）
# indent=4     → 每層縮排 4 個空格，使輸出更易讀
# sort_keys=True → 將 key 按字母順序排列，方便比對與閱讀
s_pretty = json.dumps(data, indent=4, sort_keys=True)
print(s_pretty)
# 輸出結果（key 依字母排序，並以縮排顯示巢狀結構）：
# {
#     "age": 30,
#     "name": "Alice",
#     "scores": [95, 87, 92]
# }

# 反序列化（JSON 字串 → Python）
# json.loads()：將 JSON 格式的「字串」解析回 Python 物件（s = string）
# JSON object {} → Python dict；JSON array [] → Python list
obj = json.loads(s)
print(type(obj), obj["name"])   # 輸出：<class 'dict'> Alice

# ── 檔案 I/O ─────────────────────────────────────────────
# 寫出到檔案
# json.dump()（無 s）：直接將 Python 物件序列化並寫入「檔案物件」
# indent=2         → 縮排 2 個空格
# ensure_ascii=False → 允許非 ASCII 字元（如中文）直接寫入，不轉為 \uXXXX 跳脫序列
with open("/tmp/data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 從檔案讀入
# json.load()（無 s）：從「檔案物件」讀取 JSON 並解析回 Python 物件
with open("/tmp/data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded)   # 輸出與原始 data 相同的 dict

# ── 型別對應 ──────────────────────────────────────────────
# JSON 與 Python 之間的型別自動對應關係：
#
# Python dict   → JSON object  {}    （鍵值對，key 必須是字串）
# Python list   → JSON array   []    （有序集合）
# Python str    → JSON string  ""    （雙引號字串）
# Python int    → JSON number        （整數，無小數點）
# Python float  → JSON number        （浮點數，有小數點）
# Python True   → JSON true          （注意：Python 首字大寫，JSON 全小寫）
# Python False  → JSON false
# Python None   → JSON null          （Python None 對應 JSON null）

print(json.dumps([1, True, None, "hello"]))
# 輸出：[1, true, null, "hello"]
# 可觀察到 True → true、None → null 的自動型別轉換

# ── 中文不跳脫 ───────────────────────────────────────────
# 預設 ensure_ascii=True 會將非 ASCII 字元（如中文）轉為 Unicode 跳脫序列 \uXXXX，
# 設為 False 則直接輸出原始字元，檔案較易閱讀但需確保以 UTF-8 儲存。
record = {"城市": "澎湖", "人口": 100000}
print(json.dumps(record, ensure_ascii=False))
# 輸出：{"城市": "澎湖", "人口": 100000}   （中文直接顯示）

print(json.dumps(record, ensure_ascii=True))
# 輸出：{"\u57ce\u5e02": "\u6f8e\u6e56", "\u4eba\u53e3": 100000}   （中文被轉為跳脫序列）
