# R12. Counter 統計 + most_common（1.12）
# ------------------------------------------------------------
# Counter 是專門做「元素次數統計」的工具。
# most_common(n) 可快速找出出現次數最多的前 n 個元素。
# ------------------------------------------------------------

from collections import Counter

words = ['look', 'into', 'my', 'eyes', 'look']
print("原始 words =", words)

word_counts = Counter(words)
print("\n初次統計結果 Counter =", word_counts)

top3 = word_counts.most_common(3)
print("出現次數前 3 名 =", top3)

print("\n更新額外詞彙 ['eyes', 'eyes']")
word_counts.update(['eyes', 'eyes'])
print("更新後 Counter =", word_counts)
print("更新後前 3 名 =", word_counts.most_common(3))
