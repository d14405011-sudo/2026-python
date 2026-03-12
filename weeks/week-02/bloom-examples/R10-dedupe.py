# R10. 去重且保序（1.10）

def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

def dedupe2(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


nums = [1, 5, 2, 1, 9, 1, 5, 10]
print("原始串列：", nums)
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
