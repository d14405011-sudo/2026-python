# R05. 數字基礎：四捨五入、精確運算、格式化與進制轉換（Cookbook 第 3.1–3.4 節）
# 本模組涵蓋：round（四捨五入）/ Decimal（精確浮點數）/ format（數字格式化）/ 
# bin/oct/hex（進制轉換）/ localcontext（Decimal 上下文設定）

from decimal import Decimal, localcontext
import math

# ── 第 3.1 節：四捨五入與 round() 函數 ────────────────────
# Python 的 round() 使用「銀行家捨入」（banker's rounding）= 四捨六入五取偶
# 即：當舍去數位為 5 時，向最近的偶數四捨五入，而不是總是往上進
print(round(1.27, 1))  # 1.3（正常四捨五入）
print(round(1.25361, 3))  # 1.254（正常四捨五入）
print(round(0.5))  # 0（5 取偶，0 是偶數，所以向零捨入）
print(round(2.5))  # 2（5 取偶，2 是偶數，所以不進位）

# 也可以對整數進行四捨五入，第二參數為負數時四捨五入到十位數、百位數等
a = 1627731
print(round(a, -2))  # 1627700（對百位四捨五入，最後兩位變 0）

# ── 第 3.2 節：精確浮點數與 Decimal 模組 ──────────────────
# float 因二進制表示的限制，會產生舍入誤差（特別是金融計算時問題嚴重）
print(4.2 + 2.1)  # 6.300000000000001（有誤差！）

# 使用 Decimal 進行精確十進制運算（從字串初始化以避免浮點轉換誤差）
da, db = Decimal("4.2"), Decimal("2.1")
print(da + db)  # 6.3（精確結果）

# 使用 localcontext() 改變 Decimal 的計算上下文（精度、取整等設定）
with localcontext() as ctx:
    ctx.prec = 3  # 設定精度為 3 位有效數字
    print(Decimal("1.3") / Decimal("1.7"))  # 0.765（按照設定精度計算）

# 當需要加總許多浮點數時，使用 math.fsum() 可以避免累積誤差
print(math.fsum([1.23e18, 1, -1.23e18]))  # 1.0（正確！普通相加會得到 0.0）

# ── 第 3.3 節：數字格式化（format() 和 f-string） ─────────
# Python 的格式化規範：[填充][對齊][符號][#][0][寬度][,][.精度][類型]
x = 1234.56789
print(format(x, "0.2f"))  # '1234.57'（固定小數點，2 位小數）
print(format(x, ">10.1f"))  # '    1234.6'（右對齊，寬度 10，1 位小數）
print(format(x, ","))  # '1,234.56789'（加千位分隔符）
print(format(x, "0,.2f"))  # '1,234.57'（千位分隔符 + 2 位小數）
print(format(x, "e"))  # '1.234568e+03'（科學記號格式）

# ── 第 3.4 節：進制轉換（二進制、八進制、十六進制） ──────
# Python 內建函數可以快速進行進制轉換
n = 1234
print(bin(n), oct(n), hex(n))  # 0b10011010010 0o2322 0x4d2（包含前綴的字串表示）
print(format(n, "b"), format(n, "x"))  # 10011010010 4d2（不含前綴的格式化表示）

# 也可以用 int() 函數指定進制基數，將字串轉換為整數
print(int("4d2", 16), int("2322", 8))  # 1234 1234（十六進制和八進制的字串轉回十進制）
