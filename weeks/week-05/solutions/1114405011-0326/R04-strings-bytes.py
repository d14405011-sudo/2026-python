# R04. 位元組字串操作（Cookbook 第 2.20 節）
# bytes / bytearray 支援大部分字串方法，但有幾個重要差異
# 位元組字串是不可變的位元組序列，主要用於二進制資料處理和網路通訊

import re

# ─── 位元組字串的基本操作 ───────────────────────────────
# 位元組字串使用 b"" 前綴定義，支援大多數字串方法（split, replace, startswith 等）
data = b"Hello World"
print(data[0:5])  # b'Hello'（切片返回新的位元組字串）
print(data.startswith(b"Hello"))  # True（檢查是否以指定位元組開頭）
print(data.split())  # [b'Hello', b'World']（使用空格分割，按空白字元分割）
print(data.replace(b"Hello", b"Hello Cruel"))  # b'Hello Cruel World'（替換所有匹配項）

# ─── 正則表達式與位元組字串 ───────────────────────────
# 當使用位元組字串時，正則表達式也必須是位元組模式（使用 rb"" 前綴）
raw = b"FOO:BAR,SPAM"
print(re.split(rb"[:,]", raw))  # [b'FOO', b'BAR', b'SPAM']（按冒號或逗號分割位元組字串）

# ─── 重要差異 1：位元組索引回傳整數而非字元 ────────────
# 字串索引返回字元（str），位元組索引返回該字節對應的整數值（0-255）
a = "Hello"
b = b"Hello"
print(a[0])  # 'H'（字元）
print(b[0])  # 72（整數，即 ord('H') 的值）

# ─── 重要差異 2：位元組字串不能直接用 format()，需先編碼 ──
# 位元組字串不支援 format() 或 f-string 格式化，需先用字串格式化再 .encode() 轉換為位元組
formatted = "{:10s} {:10d}".format("ACME", 100).encode("ascii")
print(formatted)  # b'ACME            100'（先格式化為字串，再編碼為位元組）
