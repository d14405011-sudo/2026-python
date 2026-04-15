# Understand（理解）- itertools 工具函數
#
# 本檔案重點：
# 1) 以 iterator 風格處理資料流，不一次建立大列表
# 2) 掌握 islice / dropwhile / takewhile / chain 的語意差異
# 3) 了解 permutations / combinations 的組合數學意義

from itertools import islice, dropwhile, takewhile, chain, permutations, combinations

print("--- islice() 切片 ---")


def count(n):
    # 無窮計數器：從 n 開始持續遞增
    i = n
    while True:
        yield i
        i += 1


c = count(0)
# islice(iterator, start, stop) 會略過前 start 個，取到 stop-1 為止
result = list(islice(c, 5, 10))
print(f"islice(c, 5, 10): {result}")

print("\n--- dropwhile() 條件跳過 ---")
nums = [1, 3, 5, 2, 4, 6]
# dropwhile(predicate, seq)：
# 只要條件為 True 就持續丟棄，直到第一次 False 後，後面全部保留
result = list(dropwhile(lambda x: x < 5, nums))
print(f"dropwhile(x<5, {nums}): {result}")

print("\n--- takewhile() 條件取用 ---")
# takewhile(predicate, seq)：
# 只取前面連續滿足條件的元素，遇到第一個 False 就停止
result = list(takewhile(lambda x: x < 5, nums))
print(f"takewhile(x<5, {nums}): {result}")

print("\n--- chain() 串聯 ---")
a = [1, 2]
b = [3, 4]
c = [5]
# chain 會把多個 iterable 串成單一資料流
print(f"chain(a, b, c): {list(chain(a, b, c))}")

print("\n--- permutations() 排列 ---")
items = ["a", "b", "c"]
# permutations(items) 預設取長度 r=len(items)，順序不同視為不同結果
print(f"permutations(items):")
for p in permutations(items):
    print(f"  {p}")

# permutations(items, 2)：從 3 個元素挑 2 個做「有序排列」
print(f"permutations(items, 2):")
for p in permutations(items, 2):
    print(f"  {p}")

print("\n--- combinations() 組合 ---")
# combinations(items, 2)：從 3 個元素挑 2 個做「無序組合」
# ('a', 'b') 與 ('b', 'a') 視為同一組，不會重複出現
print(f"combinations(items, 2):")
for c in combinations(items, 2):
    print(f"  {c}")

print("\n--- 組合應用：密碼窮舉 ---")
chars = ["A", "B", "1"]
print("2位數密碼:")
# 這裡用 permutations(chars, 2)：不允許重複字元，且順序有差
for p in permutations(chars, 2):
    print(f"  {''.join(p)}")

print("2位數密碼（可重複）:")
from itertools import combinations_with_replacement

# combinations_with_replacement 允許重複，但仍是「組合」觀念（不考慮順序）
for p in combinations_with_replacement(chars, 2):
    print(f"  {''.join(p)}")
