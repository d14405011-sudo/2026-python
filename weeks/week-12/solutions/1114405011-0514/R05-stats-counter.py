# R05. 資料統計與累加（6.13）
# Counter / defaultdict / namedtuple 整合應用
#
# 本範例示範 collections 模組中三個非常常用的工具：
# 1) Counter：快速統計元素出現次數
# 2) defaultdict：自動提供預設值，避免 KeyError
# 3) namedtuple：讓 tuple 具有欄位名稱，可讀性更高

from collections import Counter, defaultdict, namedtuple

# ── Counter：計數器 ──────────────────────────────────────
# 準備一串單字資料，故意重複多次，方便觀察計數效果。
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
# Counter 會自動統計每個元素出現次數，結果類似 dict。
cnt = Counter(words)
print("Counter：", cnt)
# most_common(n) 會回傳出現次數最高的前 n 名，格式為 [(元素, 次數), ...]
print("最多出現：", cnt.most_common(2))      # [('apple', 3), ('banana', 2)]

# 可直接相加合併
# Counter 支援加法：同鍵值的次數會相加，適合整合不同批次統計結果。
extra = Counter(["banana", "cherry"])
print("合併：", cnt + extra)

# ── defaultdict：有預設值的 dict ─────────────────────────
# 按類別分組
# 假設這是 (系所, 姓名) 的原始資料。
records = [
    ("系資", "Alice"),
    ("電子", "Bob"),
    ("系資", "Carol"),
    ("電子", "David"),
    ("系資", "Eve"),
]

# defaultdict(list) 代表：
# - 當 key 首次出現時，自動建立一個空 list 當預設值
# - 可直接 append，不需先寫 if key not in dict
by_dept = defaultdict(list)
for dept, name in records:
    by_dept[dept].append(name)

print("\ndefaultdict：")
for dept, members in by_dept.items():
    print(f"  {dept}: {members}")

# defaultdict(int) 做計數
# int() 的預設值是 0，因此適合用來累加計分或計次。
score_sum = defaultdict(int)
scores = [("Alice", 90), ("Bob", 80), ("Alice", 85), ("Bob", 70)]
for name, score in scores:
# 第一次遇到某人時，score_sum[name] 會自動是 0，接著再加上分數。
    score_sum[name] += score
# defaultdict 印出來會帶型別資訊，轉成 dict 可讓輸出更簡潔。
print("\n各人總分：", dict(score_sum))

# ── namedtuple：具名結構，更可讀 ─────────────────────────
# namedtuple 可視為「不可變（immutable）的輕量資料物件」：
# - 保留 tuple 的輕量特性
# - 但可以用欄位名稱存取（s.symbol）而非索引（s[0]）
Stock = namedtuple("Stock", ["symbol", "price", "change"])
s = Stock("AA", 39.48, -0.18)
print(f"\n{s.symbol}: ${s.price}  漲跌 {s.change}")

# ── 綜合：從 list of dict 做統計 ─────────────────────────
# 這裡示範常見資料格式：list 裡每筆是 dict（例如從 JSON 讀入）。
data = [
    {"dept": "系資", "score": 85},
    {"dept": "電子", "score": 78},
    {"dept": "系資", "score": 92},
    {"dept": "電子", "score": 88},
]

# 目標：依系所分組收集分數，最後計算各系平均。
dept_scores = defaultdict(list)
for row in data:
    dept_scores[row["dept"]].append(row["score"])

print("\n各系平均：")
for dept, scores in dept_scores.items():
# 平均 = 總和 / 筆數
    avg = sum(scores) / len(scores)
# :.1f 代表格式化成小數點後 1 位
    print(f"  {dept}: {avg:.1f}")
