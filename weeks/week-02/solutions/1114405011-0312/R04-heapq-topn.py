# R4. heapq 取 Top-N（1.4）

import heapq

# 1) nlargest / nsmallest 可以直接從一般 list 取前 N 大或前 N 小。
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print("原始 nums:", nums)
print("Top 3 最大:", heapq.nlargest(3, nums))
print("Top 3 最小:", heapq.nsmallest(3, nums))

# 2) 對複雜資料可用 key 指定比較欄位。
# 這裡依照 price 找出最便宜的 1 筆股票資料。
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
]
print("價格最低的 1 檔:", heapq.nsmallest(1, portfolio, key=lambda s: s['price']))

# 3) heapify 會把 list 原地轉成最小堆（min-heap）。
# 最小值會放在根節點位置（索引 0）。
heap = list(nums)
heapq.heapify(heap)
print("heapify 後:", heap)
# heappop 每次都會取出目前最小值。
print("heappop 取出:", heapq.heappop(heap))
print("heappop 後 heap:", heap)
