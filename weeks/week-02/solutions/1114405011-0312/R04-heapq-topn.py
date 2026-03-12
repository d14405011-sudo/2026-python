# R4. heapq 取 Top-N（1.4）

import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print("原始 nums:", nums)
print("Top 3 最大:", heapq.nlargest(3, nums))
print("Top 3 最小:", heapq.nsmallest(3, nums))

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
]
print("價格最低的 1 檔:", heapq.nsmallest(1, portfolio, key=lambda s: s['price']))

heap = list(nums)
heapq.heapify(heap)
print("heapify 後:", heap)
print("heappop 取出:", heapq.heappop(heap))
print("heappop 後 heap:", heap)
