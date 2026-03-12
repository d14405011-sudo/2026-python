# R5. 優先佇列 PriorityQueue（1.5）
# ------------------------------------------------------------
# 這裡用 heapq 實作「高優先級先出」的佇列。
# 因為 heapq 是最小堆，所以把 priority 取負號：
# priority 越大 -> -priority 越小 -> 越早被彈出。
# _index 用來處理同優先級時的先進先出（FIFO）順序。
# ------------------------------------------------------------

import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        # tuple 結構：(-優先級, 插入序, 實際資料)
        heapq.heappush(self._queue, (-priority, self._index, item))
        print(f"push(item={item}, priority={priority}) 後 heap = {self._queue}")
        self._index += 1

    def pop(self):
        popped = heapq.heappop(self._queue)[-1]
        print(f"pop() 取出 {popped}；剩餘 heap = {self._queue}")
        return popped


print("=== PriorityQueue 示範 ===")
pq = PriorityQueue()

pq.push('low', 1)
pq.push('medium', 3)
pq.push('high', 5)
pq.push('medium-later', 3)

print("\n依優先級出佇列（高 -> 低；同級依先進先出）")
print("第 1 次 pop 結果 =", pq.pop())
print("第 2 次 pop 結果 =", pq.pop())
print("第 3 次 pop 結果 =", pq.pop())
print("第 4 次 pop 結果 =", pq.pop())
