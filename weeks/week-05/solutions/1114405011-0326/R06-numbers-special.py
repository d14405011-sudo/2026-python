# R06. 特殊數值：無窮大、NaN、分數與隨機選擇（Cookbook 第 3.7–3.11 節）
# 內容涵蓋：float 無窮大和 NaN / fractions.Fraction（精確分數）/ random（隨機模組）

import math
import random
from fractions import Fraction

# ── 第 3.7 節：無窮大（inf）與非數字值（NaN） ──────────────
# float 支援特殊值：正無窮大、負無窮大、非數字（NaN）
a = float("inf")      # 正無窮大
b = float("-inf")     # 負無窮大
c = float("nan")      # NaN（Not a Number）
print(a, b, c)  # inf -inf nan

# 檢驗特殊值的正確方式（不能用 == 比較）
print(math.isinf(a))  # True（檢查是否為無窮大）
print(math.isnan(c))  # True（檢查是否為 NaN）

# 無窮大的數學運算
print(a + 45, 10 / a)  # inf 0.0（無窮大 + 有限數仍為無窮大；有限數 / 無窮大 = 0）
print(a / a, a + b)  # nan nan（無窮大 / 無窮大 和 無窮大 + (-無窮大) 都是未定義）

# NaN 的特殊性質：NaN 不等於自己（這是 IEEE 浮點數標準的要求）
print(c == c)  # False（NaN == NaN 永遠為 False！）
print(c == float("nan"))  # False（任何 NaN 都不相等）

# ── 第 3.8 節：分數運算（Fraction 類） ─────────────────────
# Fraction 提供精確的有理數（分數）運算，自動化簡
p = Fraction(5, 4)      # 5/4（分子/分母）
q = Fraction(7, 16)     # 7/16
r = p * q               # 35/64
print(p + q)  # 27/16（自動通分並化簡）
print(r.numerator, r.denominator)  # 35 64（分子和分母）
print(float(r))  # 0.546875（轉換為浮點數）

# limit_denominator() 可以找最接近的分數，限制分母大小
print(r.limit_denominator(8))  # 4/7（在分母 ≤ 8 的範圍內找最接近的分數）

# 從浮點數的確切表示建立分數（避免浮點誤差）
print(Fraction(*(3.75).as_integer_ratio()))  # 15/4（3.75 的精確分數表示）

# ── 第 3.11 節：隨機選擇與 random 模組 ──────────────────
# random 模組提供各種隨機操作（注意：不適合密碼學安全場景）
values = [1, 2, 3, 4, 5, 6]
print(random.choice(values))  # 隨機選擇一個元素
print(random.sample(values, 3))  # 隨機選擇 3 個不重複的元素

random.shuffle(values)          # 在原地打亂列表（會改變原列表）
print(values)  # 打亂後的序列

print(random.randint(0, 10))  # 回傳 0~10 的隨機整數（包含端點）

# 設定隨機種子使結果可重現（用於測試和除錯）
random.seed(42)  # 相同的種子會產生相同的隨機序列
print(random.random())  # 0.6394267984578837（來自種子 42）
