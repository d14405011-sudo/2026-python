# U03. 字串格式化效能與陷阱（Cookbook 第 2.14–2.20 節）
# 內容涵蓋：join vs +（效能差異）/ format_map 處理缺失鍵 / bytes 索引差異 / 格式化陷阱

import timeit

# ── join 效能優於 + （2.14）──────────────────────────
# 字串串接時，不應該用 += 迴圈拼接，因為每次都會建立新字串（O(n²) 複雜度）
# 應該收集所有部分後，一次用 join() 連接（O(n) 複雜度）

parts = [f"item{i}" for i in range(1000)]


def bad_concat():
    """【不好的做法】每次 += 都會建立新字串，效率極低"""
    s = ""
    for p in parts:
        s += p  # 每次建立新字串，複雜度 O(n²)
    return s


def good_join():
    """【好的做法】一次性分配記憶體，效率高"""
    return "".join(parts)  # 一次分配，複雜度 O(n)


t1 = timeit.timeit(bad_concat, number=500)
t2 = timeit.timeit(good_join, number=500)
print(f"+串接: {t1:.3f}s  join: {t2:.3f}s")


# ── format_map 處理缺失鍵（2.15）─────────────────────
# format_map() 與 format() 兩者的差異：
# - format() 使用 {key} 佔位符，如果字典中缺少 key 會報 KeyError
# - format_map() 搭配自訂 dict 子類，可以在缺失時自訂行為（例如保留佔位符）

class SafeSub(dict):
    """自訂字典子類，缺失鍵時不報錯，而是保留原佔位符"""
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"  # 缺失時保留佔位符（例如 {n}）


name = "Guido"
s = "{name} has {n} messages."
print(s.format_map(SafeSub(vars())))  # 'Guido has {n} messages.'
# 注意：name 存在所以被替換、n 不存在所以保留原佔位符 {n}，不報錯

# ── bytes 索引回傳整數（2.20）────────────────────────
# 字串與位元組字串的索引行為不同：
# - 字串索引回傳：字元（str）
# - 位元組字串索引回傳：該字節的整數值 (0-255)

a = "Hello"
b = b"Hello"
print(a[0])  # 'H'（字元）
print(b[0])  # 72（整數 = ord('H')）

# 位元組字串不能直接 format，必須先格式化成字串再 encode
print("{:10s} {:5d}".format("ACME", 100).encode("ascii"))
# b'ACME            100'（先格式化為字串，再編碼成位元組字串）
