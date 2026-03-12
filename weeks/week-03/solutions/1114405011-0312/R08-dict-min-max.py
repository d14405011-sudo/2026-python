# R8. 字典運算：min/max/sorted + zip（1.8）
# ------------------------------------------------------------
# 字典常見需求：
# 1. 找最小/最大 value 對應的 key。
# 2. 依 value 排序。
# zip(prices.values(), prices.keys()) 會產生 (value, key) 配對。
# ------------------------------------------------------------

prices = {'ACME': 45.23, 'AAPL': 612.78, 'FB': 10.75}
print("原始 prices =", prices)

print("\n=== 用 zip(value, key) 做比較 ===")
pairs = list(zip(prices.values(), prices.keys()))
print("配對後 pairs =", pairs)

min_pair = min(pairs)
max_pair = max(pairs)
sorted_pairs = sorted(pairs)

print("最小 pair =", min_pair)
print("最大 pair =", max_pair)
print("排序後 pairs =", sorted_pairs)


print("\n=== 直接對 key 比較（以 value 當 key）===")
min_key = min(prices, key=lambda k: prices[k])
max_key = max(prices, key=lambda k: prices[k])

print("最小價格股票代號 =", min_key, ", 價格 =", prices[min_key])
print("最大價格股票代號 =", max_key, ", 價格 =", prices[max_key])
