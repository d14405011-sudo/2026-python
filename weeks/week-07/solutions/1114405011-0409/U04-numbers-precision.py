# U04. 數字精度的陷阱與選擇（3.1–3.7）
#
# 實務上最常見的數值雷點：
# 1) round() 不是你以為的傳統四捨五入（而是銀行家捨入）。
# 2) NaN 與任何值比較都不成立，連自己都不相等。
# 3) float 與 Decimal 的取捨：速度 vs 精確度。

import math
import timeit
from decimal import Decimal, ROUND_HALF_UP

# ── 銀行家捨入（3.1）─────────────────────────────────
# Python round() 採用「四捨六入五取偶」(banker's rounding)，
# 目的是在大量統計中降低整體偏差，不是日常口語的四捨五入。
print(round(0.5))  # 0（不是 1！）
print(round(2.5))  # 2（不是 3！）
print(round(3.5))  # 4


# 若你在金融、計費、發票等場景需要「傳統四捨五入」，
# 請改用 Decimal 並指定 ROUND_HALF_UP。
def trad_round(x: float, n: int = 0) -> Decimal:
    # 先用 str(x) 避免把二進位浮點誤差帶入 Decimal
    d = Decimal(str(x))
    # n=0 代表整數位；n>0 代表小數位
    fmt = Decimal("1") if n == 0 else Decimal("0." + "0" * n)
    return d.quantize(fmt, rounding=ROUND_HALF_UP)


print(trad_round(0.5))  # 1
print(trad_round(2.5))  # 3

# ── NaN 無法用 == 比較（3.7）─────────────────────────
# IEEE 754 定義中，NaN 代表「不是一個有效數值」，
# 因此與任何值比較（包含自己）都會是 False。
c = float("nan")
print(c == c)  # False（自己不等於自己！）
print(c == float("nan"))  # False
print(math.isnan(c))  # True（唯一正確的檢測方式）

data = [1.0, float("nan"), 3.0, float("nan"), 5.0]
# 清洗資料時，記得用 isnan 過濾掉無效值
clean = [x for x in data if not math.isnan(x)]
print(clean)  # [1.0, 3.0, 5.0]

# ── float vs Decimal 選擇（3.2）──────────────────────
# float：速度快，但小數是二進位近似值，常有極小誤差
# 適用：科學計算、圖形、模擬等容許誤差場景
print(0.1 + 0.2)  # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False

# Decimal：十進位精確，代價是運算速度較慢
# 適用：金額、稅率、會計、對帳等要求精準場景
print(Decimal("0.1") + Decimal("0.2"))  # 0.3
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))  # True

t1 = timeit.timeit(lambda: 0.1 * 999, number=100_000)
t2 = timeit.timeit(lambda: Decimal("0.1") * 999, number=100_000)
print(f"float: {t1:.3f}s  Decimal: {t2:.3f}s（Decimal 約慢 {t2 / t1:.0f} 倍）")
