# U04. 數字精度的陷阱與選擇（Cookbook 第 3.1–3.7 節）
# 內容涵蓋：銀行家捨入與傳統四捨五入的差異 / NaN 比較陷阱 / float vs Decimal 選擇

import math
import timeit
from decimal import Decimal, ROUND_HALF_UP

# ── 銀行家捨入（3.1）─────────────────────────────────
# Python 的 round() 函數使用「四捨六入五取偶」（banker's rounding）
# 即：當捨去數位為 5 時，向最近的偶數四捨五入（而非總是進位）
# 這與日常生活中的「四捨五入」不同！

print(round(0.5))  # 0（不是 1！5 向最近偶數進 → 0 是偶數）
print(round(2.5))  # 2（不是 3！5 向最近偶數進 → 2 是偶數）
print(round(3.5))  # 4（不是 4！5 向最近偶數進 → 4 是偶數）


# 若需傳統四捨五入，使用 Decimal + ROUND_HALF_UP
def trad_round(x: float, n: int = 0) -> Decimal:
    """傳統四捨五入（四捨五進）"""
    d = Decimal(str(x))  # 先轉成字串再到 Decimal，避免浮點誤差
    fmt = Decimal("1") if n == 0 else Decimal("0." + "0" * n)
    return d.quantize(fmt, rounding=ROUND_HALF_UP)


print(trad_round(0.5))  # 1（傳統捨入）
print(trad_round(2.5))  # 3（傳統捨入）

# ── NaN 無法用 == 比較（3.7）─────────────────────────
# NaN（Not a Number）是特殊的浮點值，它有特殊性質：NaN 不等於自己！
# 這是 IEEE 浮點標準的要求，用於區別未定義的計算結果

c = float("nan")
print(c == c)  # False（NaN != NaN，這很反直覺！）
print(c == float("nan"))  # False（任何 NaN 都不相等）
print(math.isnan(c))  # True（唯一正確的檢測方式）

# 正確清理包含 NaN 的列表
data = [1.0, float("nan"), 3.0, float("nan"), 5.0]
clean = [x for x in data if not math.isnan(x)]  # 用 math.isnan() 檢測
print(clean)  # [1.0, 3.0, 5.0]

# ── float vs Decimal 選擇（3.2）──────────────────────
# float：快速但有誤差（適合科學/工程計算）
print(0.1 + 0.2)  # 0.30000000000000004（有誤差）
print(0.1 + 0.2 == 0.3)  # False（因為誤差，相等性比較失敗）

# Decimal：精確但慢（適合金融/會計計算）
print(Decimal("0.1") + Decimal("0.2"))  # 0.3（完全精確）
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))  # True（相等性正確）

# 效能對比
t1 = timeit.timeit(lambda: 0.1 * 999, number=100_000)
t2 = timeit.timeit(lambda: Decimal("0.1") * 999, number=100_000)
print(f"float: {t1:.3f}s  Decimal: {t2:.3f}s（Decimal 約慢 {t2 / t1:.0f} 倍）")
