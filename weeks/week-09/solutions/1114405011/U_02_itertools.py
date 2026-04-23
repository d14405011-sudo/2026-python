# Understand（理解）- itertools 工具函數

# 從 itertools 模組中匯入常用的迭代器工具：
# islice: 用於對無限或一般迭代器進行切片（類似 [start:stop] 的操作）
# dropwhile: 只要條件為真，就一直丟棄元素；一旦條件為假，就開始回傳剩餘的所有元素
# takewhile: 只要條件為真，就一直回傳元素；一旦遇到條件為假，就停止回傳
# chain: 將多個可迭代物件（如串列）串聯在一起，視為單一連續的迭代器
# permutations: 產生指定長度的所有可能的排列（考慮順序）
# combinations: 產生指定長度的所有可能的組合（不考慮順序）
from itertools import islice, dropwhile, takewhile, chain, permutations, combinations

print("--- islice() 切片 ---")


# 定義一個產生器函數，會無限產生從 n 開始的遞增整數
def count(n):
    i = n
    while True:
        yield i
        i += 1


c = count(0)  # 建立一個從 0 開始的無限產生器
# islice(迭代器, 起始索引, 結束索引)
# 從這個無限的產生器中，取出第 5 個到第 9 個元素 (索引 5 到 9)
result = list(islice(c, 5, 10))
print(f"islice(c, 5, 10): {result}")

print("\n--- dropwhile() 條件跳過 ---")
nums = [1, 3, 5, 2, 4, 6]
# dropwhile 會略過前面滿足條件 (x < 5) 的元素
# 但只要遇到第一個不滿足條件的元素 (5)，後面的元素不論是否滿足條件都會全部留下 (包含後面的 2, 4, 6)
result = list(dropwhile(lambda x: x < 5, nums))
print(f"dropwhile(x<5, {nums}): {result}")

print("\n--- takewhile() 條件取用 ---")
# takewhile 會一直收集滿足條件 (x < 5) 的元素
# 一旦遇到第一個不滿足條件的元素 (5)，就會立刻停止收集並結束
result = list(takewhile(lambda x: x < 5, nums))
print(f"takewhile(x<5, {nums}): {result}")

print("\n--- chain() 串聯 ---")
a = [1, 2]
b = [3, 4]
c = [5]
# chain 可以將多個被分開的串列 (a, b, c) 當成一個連續的迭代器來走訪，而不需要真的去串接配置新的大串列
print(f"chain(a, b, c): {list(chain(a, b, c))}")

print("\n--- permutations() 排列 ---")
items = ["a", "b", "c"]
print(f"permutations(items):")
# 未指定長度時，預設會產生所有元素的全排列 (A3取3 = 6 種)
for p in permutations(items):
    print(f"  {p}")

print(f"permutations(items, 2):")
# 從中取出 2 個元素進行排列 (A3取2 = 6 種)
# 因為是「排列」，順序不同視為不同結果 (例如 ('a', 'b') 和 ('b', 'a') 被視為相異)
for p in permutations(items, 2):
    print(f"  {p}")

print("\n--- combinations() 組合 ---")
print(f"combinations(items, 2):")
# 從中取出 2 個元素進行組合 (C3取2 = 3 種)
# 因為是「組合」，不考慮順序 (例如出現過 ('a', 'b') 之後，就不會再出現 ('b', 'a'))
for c in combinations(items, 2):
    print(f"  {c}")

print("\n--- 組合應用：密碼窮舉 ---")
chars = ["A", "B", "1"]
print("2位數密碼:")
# 使用 permutations 來窮舉所有不重複字元的排列密碼
for p in permutations(chars, 2):
    print(f"  {''.join(p)}")

print("2位數密碼（可重複）:")
# 匯入 combinations_with_replacement，用於產生允許字元重複選取的「組合」
from itertools import combinations_with_replacement

# 允許元素重複出現 (例如可以抽出 ('A', 'A'), ('B', 'B'))，同樣是不考量順序
for p in combinations_with_replacement(chars, 2):
    print(f"  {''.join(p)}")
