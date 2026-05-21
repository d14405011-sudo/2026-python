# A01. functools.partial：固定參數，減少重複
# 當你一直用「幾乎相同」的參數呼叫同一個函數，partial 幫你省掉重複
# 對應 Bloom's Taxonomy：應用（Apply）— 能把技巧套到新情境


# 匯入 partial：用來固定部分參數，產生新函數
from functools import partial

# ── 基本概念：固定部分參數，產生新函數 ───────────────────


# 定義一個計算次方的函數
def power(base, exp):
    return base ** exp  # 回傳 base 的 exp 次方


# 用 partial 固定 exp=2，產生只需填 base 的新函數 square
square = partial(power, exp=2)   # 固定 exp=2，只剩 base 要填
# 用 partial 固定 exp=3，產生 cube
cube   = partial(power, exp=3)   # 固定 exp=3


print("=== partial 基本用法 ===")
print(square(5))    # 等同 power(5, 2)，結果 25
print(cube(3))      # 等同 power(3, 3)，結果 27
# 用 square 產生 1~5 的平方
print([square(n) for n in range(1, 6)])  # [1, 4, 9, 16, 25]

# ── 搭配 sorted：固定排序的 key ──────────────────────────


# 建立學生資料，每個學生有姓名、數學、英文成績
students = [
    {"name": "王小明", "math": 80, "english": 70},
    {"name": "李大華", "math": 65, "english": 90},
    {"name": "張三",   "math": 95, "english": 55},
]


# 取得指定學生某科成績
def get_score(student, subject):
    return student[subject]


# 用 partial 固定 subject，產生排序用的 key 函數
by_math    = partial(get_score, subject="math")
by_english = partial(get_score, subject="english")


print("\n=== partial 搭配 sorted ===")
# 用 by_math 當 key 排序，reverse=True 代表高分在前
print("數學排名：", [s["name"] for s in sorted(students, key=by_math,    reverse=True)])
# 用 by_english 當 key 排序
print("英文排名：", [s["name"] for s in sorted(students, key=by_english, reverse=True)])

# ── CPE 應用：UVA 11005 進位制成本 ──────────────────────
# 題目需要計算同一個數字在不同進位下的成本
# 用 partial 固定「成本表」，讓程式碼更簡潔


# 定義所有可能的數字字元（0-9, A-Z）
DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# 計算數字 n 在 base 進位下，每一位的成本總和
def cost_in_base(n, base, costs):
    """計算 n 在 base 進位下每一位數字的成本總和"""
    if n == 0:
        return costs[0]  # n=0 時只算一位
    total = 0
    while n > 0:
        total += costs[n % base]  # 取出最低位數字，加上對應成本
        n //= base                # 去掉最低位，繼續處理下一位
    return total

# 假設每個字元成本都是 1（示範用）

# 假設每個字元成本都是 1（示範用）
uniform_costs = [1] * 36

# 用 partial 固定 costs，之後只要填 (n, base)

# 用 partial 固定 costs 參數，產生只需填 n, base 的新函數 calc
calc = partial(cost_in_base, costs=uniform_costs)

print("\n=== UVA 11005：各進位下的成本 ===")

# 計算數字 n 在 2~36 進位下的最低成本與最佳進位
n = 255
best_cost = min(calc(n, b) for b in range(2, 37))
best_bases = [b for b in range(2, 37) if calc(n, b) == best_cost]
print(f"數字 {n}，最低成本 {best_cost}，最佳進位：{best_bases}")

# ── 固定 print 的格式 ─────────────────────────────────────
# 競程輸出時常用


# 用 partial 固定 print 的 end 參數，讓每次 print 不自動換行
print_same_line = partial(print, end=" ")
print("\n=== 同行輸出 ===")
for i in range(1, 6):
    print_same_line(i)  # 會同行輸出 1 2 3 4 5
print()   # 最後補一個換行

# ── partial vs lambda 比較 ────────────────────────────────
# 兩種寫法效果一樣，partial 可讀性更高


# lambda 與 partial 寫法比較：兩者都能產生平方函數
square_lambda  = lambda x: power(x, 2)         # lambda 寫法
square_partial = partial(power, exp=2)         # partial 寫法


print("\n=== lambda vs partial ===")
# 兩種寫法結果都一樣
print([square_lambda(n)  for n in range(1, 6)])   # [1, 4, 9, 16, 25]
print([square_partial(n) for n in range(1, 6)])   # [1, 4, 9, 16, 25]

# 記憶重點 ──────────────────────────────────────────────────
# partial(函數, 固定的參數) → 回傳新函數，只剩剩餘的參數要填
# 常用場景：sorted key、min/max key、print 格式、重複呼叫某個函數
# 和 lambda 效果類似，但 partial 更清楚表達「固定哪個參數」
#
# 建議：當你想「重複呼叫同一個函數，但有些參數都一樣」時，優先考慮 partial！
