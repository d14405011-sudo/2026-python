# R5. 優先佇列 PriorityQueue（1.5）

import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
    def pop(self):
        return heapq.heappop(self._queue)[-1]


q = PriorityQueue()
q.push('foo', 1)
q.push('bar', 5)
q.push('spam', 4)
q.push('grok', 1)

print("目前內部 heap:", q._queue)
print("第 1 次 pop:", q.pop())
print("第 2 次 pop:", q.pop())
print("第 3 次 pop:", q.pop())
print("第 4 次 pop:", q.pop())
