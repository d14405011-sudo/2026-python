# R12. Counter 統計 + most_common（1.12）

from collections import Counter

# 1) Counter 會自動統計每個元素出現次數。
words = ['look', 'into', 'my', 'eyes', 'look']
word_counts = Counter(words)
print("原始單字串列：", words)
print("Counter 統計結果：", word_counts)
# most_common(n) 取出出現次數前 n 名，格式是 (元素, 次數)。
print("出現次數前 3 名：", word_counts.most_common(3))

# 2) update 可再追加新資料到原本統計中。
word_counts.update(['eyes', 'eyes'])
print("更新後的 Counter：", word_counts)
print("更新後前 3 名：", word_counts.most_common(3))
