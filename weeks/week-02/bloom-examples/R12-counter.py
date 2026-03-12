# R12. Counter 統計 + most_common（1.12）

from collections import Counter

words = ['look', 'into', 'my', 'eyes', 'look']
word_counts = Counter(words)
print("原始單字串列：", words)
print("Counter 統計結果：", word_counts)
print("出現次數前 3 名：", word_counts.most_common(3))

word_counts.update(['eyes', 'eyes'])
print("更新後的 Counter：", word_counts)
print("更新後前 3 名：", word_counts.most_common(3))
