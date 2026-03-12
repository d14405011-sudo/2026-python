# R3. deque 保留最後 N 筆（1.3）

from collections import deque

q = deque(maxlen=3)
q.append(1); q.append(2); q.append(3)
print("maxlen=3 初始:", q)
q.append(4)  # 自動丟掉最舊的 1
print("append(4) 後:", q)

q = deque()
q.append(1); q.appendleft(2)
print("append 與 appendleft 後:", q)
q.pop(); q.popleft()
print("pop 與 popleft 後:", q)
