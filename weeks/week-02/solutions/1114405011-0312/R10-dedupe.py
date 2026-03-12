# R10. 去重且保序（1.10）

# 1) 基本去重：適用於可雜湊（hashable）元素，如 int、str、tuple。
# 核心作法：用 seen 記錄看過的值，沒看過才 yield。
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

# 2) 進階去重：可提供 key，把「不可雜湊」資料轉成可比較鍵值。
# 例如 dict 本身不能放進 set，但可用 (x, y) 或 x 當 key。
def dedupe2(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


nums = [1, 5, 2, 1, 9, 1, 5, 10]
print("原始串列：", nums)
# list(...) 會把 generator 一次展開，便於觀察結果。
print("dedupe 去重後：", list(dedupe(nums)))

records = [
    {'x': 1, 'y': 2},
    {'x': 1, 'y': 3},
    {'x': 1, 'y': 2},
    {'x': 2, 'y': 4},
]
print("原始字典串列：", records)
print("依 (x, y) 去重後：", list(dedupe2(records, key=lambda d: (d['x'], d['y']))))
print("只依 x 去重後：", list(dedupe2(records, key=lambda d: d['x'])))
