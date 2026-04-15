# U03. 字串格式化效能與陷阱（2.14–2.20）
#
# 本檔覆蓋三個常見面向：
# 1) 大量字串串接時，'+' 與 ''.join() 的複雜度差異。
# 2) format_map() 遇到缺失鍵時，如何避免 KeyError。
# 3) str 與 bytes 在索引與格式化上的關鍵差異。

import timeit

# ── join 效能優於 + （2.14）──────────────────────────
# 在迴圈中做 s += p 會反覆建立新字串，成本接近 O(n^2)。
# ''.join(parts) 會一次配置結果字串，通常是 O(n)。
#
# 當資料量變大，效能差距會非常明顯。
parts = [f"item{i}" for i in range(1000)]


def bad_concat():
    s = ""
    for p in parts:
        s += p  # 每次都產生新物件，舊內容也要被複製
    return s


def good_join():
    return "".join(parts)  # 先知道所有片段，再一次組裝


t1 = timeit.timeit(bad_concat, number=500)
t2 = timeit.timeit(good_join, number=500)
print(f"+串接: {t1:.3f}s  join: {t2:.3f}s")


# ── format_map 處理缺失鍵（2.15）─────────────────────
# 一般 format() 遇到缺失鍵會直接 KeyError。
# 透過 dict.__missing__ 可定義「找不到鍵時」的行為。
class SafeSub(dict):
    def __missing__(self, key: str) -> str:
        # 這裡選擇保留原樣，方便後續再補值或偵錯
        return "{" + key + "}"


name = "Guido"
s = "{name} has {n} messages."
print(s.format_map(SafeSub(vars())))  # 'Guido has {n} messages.'（n 不存在也不報錯）

# ── bytes 索引回傳整數（2.20）────────────────────────
# 這點非常重要：
# - str[0] 取得的是「字元」
# - bytes[0] 取得的是「0~255 的整數值」
#
# 若要把 bytes 轉回字串，需要 decode()。
a = "Hello"
b = b"Hello"
print(a[0])  # 'H'（字元）
print(b[0])  # 72（整數 = ord('H')）

# bytes 不能直接使用字串格式化語法，
# 常見作法是「先格式化成 str，再 encode 成 bytes」。
print("{:10s} {:5d}".format("ACME", 100).encode("ascii"))
# b'ACME            100'
