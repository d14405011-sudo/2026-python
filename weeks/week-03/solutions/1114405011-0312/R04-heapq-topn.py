# R4. heapq 取 Top-N（1.4）
# ------------------------------------------------------------
# heapq 重點：
# 1. nlargest / nsmallest 可快速取前 N 大或前 N 小。
# 2. 可搭配 key 指定比較欄位（例如字典中的 price）。
# 3. heapify 可原地把 list 轉成最小堆（min-heap）。
# ------------------------------------------------------------

import heapq

print("=== 範例 1：數字取 Top-N ===")
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print("原始 nums =", nums)

largest_3 = heapq.nlargest(3, nums)
smallest_3 = heapq.nsmallest(3, nums)
print("前三大 nlargest(3) =", largest_3)
print("前三小 nsmallest(3) =", smallest_3)


print("\n=== 範例 2：字典資料依 price 比較 ===")
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
]
print("原始 portfolio =", portfolio)

cheapest = heapq.nsmallest(1, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(1, portfolio, key=lambda s: s['price'])
print("最便宜標的 =", cheapest)
print("最昂貴標的 =", expensive)


print("\n=== 範例 3：heapify 與 heappop ===")
heap = list(nums)
print("複製成 heap 前 =", heap)

heapq.heapify(heap)
print("heapify 後（最小堆結構）=", heap)

pop1 = heapq.heappop(heap)
print("第一次 heappop() =", pop1, "; 剩餘 heap =", heap)

pop2 = heapq.heappop(heap)
print("第二次 heappop() =", pop2, "; 剩餘 heap =", heap)
