# R3. deque 保留最後 N 筆（1.3）

from collections import deque

# 1) 設定 maxlen=3：deque 最多只保留 3 筆。
# 當超過容量時，會自動從另一端丟掉最舊元素。
q = deque(maxlen=3)
q.append(1); q.append(2); q.append(3)
print("maxlen=3 初始:", q)
q.append(4)  # 自動丟掉最舊的 1
print("append(4) 後:", q)

# 2) 不設定 maxlen 時，deque 可視為雙端佇列。
# append/appendleft 分別從右邊與左邊加入元素。
q = deque()
q.append(1); q.appendleft(2)
print("append 與 appendleft 後:", q)
# pop/popleft 分別從右邊與左邊取出元素。
q.pop(); q.popleft()
print("pop 與 popleft 後:", q)
