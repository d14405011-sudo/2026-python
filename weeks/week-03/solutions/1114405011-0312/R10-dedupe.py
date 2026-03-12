# R10. 去重且保序（1.10）
# ------------------------------------------------------------
# 目標：
# 1. 去除重複資料
# 2. 保留原本出現順序
# ------------------------------------------------------------


def dedupe(items):
    """對可雜湊（hashable）元素去重，保留順序。"""
    seen = set()
    for item in items:
        print(f"[dedupe] 檢查 item={item}，目前 seen={seen}")
        if item not in seen:
            print(f"[dedupe] -> 新元素，輸出 {item}")
            yield item
            seen.add(item)
        else:
            print(f"[dedupe] -> 重複元素，略過 {item}")


def dedupe2(items, key=None):
    """對不可雜湊元素（例如 dict）用 key 函式定義去重依據。"""
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        print(f"[dedupe2] 檢查 item={item}，比較鍵 val={val}，目前 seen={seen}")
        if val not in seen:
            print(f"[dedupe2] -> 新元素，輸出 {item}")
            yield item
            seen.add(val)
        else:
            print(f"[dedupe2] -> 重複元素，略過 {item}")


print("=== 範例 1：數字去重且保序 ===")
nums = [1, 5, 2, 1, 9, 1, 5, 10]
print("原始 nums =", nums)
unique_nums = list(dedupe(nums))
print("去重後 unique_nums =", unique_nums)


print("\n=== 範例 2：字典資料以 (x, y) 當去重鍵 ===")
rows = [
    {'x': 1, 'y': 2},
    {'x': 1, 'y': 3},
    {'x': 1, 'y': 2},
    {'x': 2, 'y': 4},
]
print("原始 rows =", rows)

unique_rows = list(dedupe2(rows, key=lambda r: (r['x'], r['y'])))
print("去重後 unique_rows =", unique_rows)
