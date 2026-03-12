# R5. 優先佇列 PriorityQueue（1.5）

import heapq

# 這個類別用 heapq 實作「高優先權先出列」的佇列。
class PriorityQueue:
    def __init__(self):
        # _queue 內部存放三元組：(-priority, index, item)
        # 使用負號是因為 heapq 預設是最小堆，我們要模擬最大優先權先出列。
        self._queue = []
        # _index 用來處理同優先權時的先後順序（先進先出）。
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        # heappop 取出三元組後，只回傳 item 本體。
        return heapq.heappop(self._queue)[-1]


q = PriorityQueue()
# bar 優先權 5 最高，spam 次之，foo/grok 同為 1。
q.push('foo', 1)
q.push('bar', 5)
q.push('spam', 4)
q.push('grok', 1)

print("目前內部 heap:", q._queue)
print("第 1 次 pop:", q.pop())
print("第 2 次 pop:", q.pop())
print("第 3 次 pop:", q.pop())
print("第 4 次 pop:", q.pop())
