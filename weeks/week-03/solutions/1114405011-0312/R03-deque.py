# R3. deque 保留最後 N 筆（1.3）
# ------------------------------------------------------------
# deque（double-ended queue）特性：
# 1. 可在左右兩端快速新增/移除元素。
# 2. 設 maxlen 後可自動維持固定長度（超出就丟最舊資料）。
# ------------------------------------------------------------

from collections import deque

print("=== 範例 1：固定長度 maxlen=3 ===")
q = deque(maxlen=3)
print("初始 q =", q)

q.append(1)
print("append(1) 後 q =", q)

q.append(2)
print("append(2) 後 q =", q)

q.append(3)
print("append(3) 後 q =", q)

# 這次再加 4，因為 maxlen=3，最左邊最舊的 1 會被自動移除
q.append(4)
print("append(4) 後 q =", q, "（最舊元素已被丟棄）")


print("\n=== 範例 2：雙端操作 appendleft / pop / popleft ===")
q = deque()
print("重設後 q =", q)

q.append(1)
print("append(1) 後 q =", q)

q.appendleft(2)
print("appendleft(2) 後 q =", q)

right_value = q.pop()
print("pop() 取出右端值 =", right_value, "; q =", q)

left_value = q.popleft()
print("popleft() 取出左端值 =", left_value, "; q =", q)
