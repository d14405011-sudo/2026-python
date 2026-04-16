# Remember（記憶）- enumerate() 和 zip()
# =========================================
# 本檔案演示 Python 中常用的疊代工具：
# 1. enumerate() - 同時取得索引和元素
# 2. zip() - 將多個可疊代物件配對在一起

colors = ["red", "green", "blue"]

# --- enumerate() 基本用法 ---
# enumerate() 會同時提供索引 i（從 0 開始）和對應的元素 color
print("--- enumerate() 基本用法 ---")
for i, color in enumerate(colors):
    print(f"{i}: {color}")

# enumerate(start=1) - 讓索引從 1 開始（而不是預設的 0）
# 適用於需要「第1個、第2個」這樣順序標記的場景
print("\n--- enumerate(start=1) ---")
for i, color in enumerate(colors, 1):
    print(f"第{i}個: {color}")

# enumerate with 檔案/文本 - 常用於讀取檔案時顯示行號
# 例如：在處理日誌檔或代碼時需要告訴使用者哪一行出錯
print("\n--- enumerate with 檔案 ---")
lines = ["line1", "line2", "line3"]
for lineno, line in enumerate(lines, 1):
    print(f"行 {lineno}: {line}")

# zip() 基本用法 - 將兩個列表的對應元素配對在一起
# zip(names, scores) 會產生：("Alice", 90), ("Bob", 85), ("Carol", 92)
print("\n--- zip() 基本用法 ---")
names = ["Alice", "Bob", "Carol"]
scores = [90, 85, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip() 多個序列 - zip() 可以同時處理 2 個、3 個或更多個序列
# 會同時迭代所有序列，每次取出一組對應的元素
print("\n--- zip() 多個序列 ---")
a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]
for x, y, z in zip(a, b, c):
    print(f"{x} + {y} + {z} = {x + y + z}")

# zip() 長度不同 - 當列表長度不同時，zip() 會在最短列表結束時停止
# 在這個例子中，x 只有 2 個元素，所以結果只包含 2 對
print("\n--- zip() 長度不同 ---")
x = [1, 2]
y = ["a", "b", "c"]
print(f"list(zip(x, y)): {list(zip(x, y))}")

# zip_longest() - 當需要配對所有元素（包括長度不同的部分）時使用
# 會用 fillvalue（預設為 None）填補較短序列的缺失值
from itertools import zip_longest

print(f"zip_longest: {list(zip_longest(x, y, fillvalue=0))}")

# 建立字典 - zip() 的實用應用之一
# dict(zip(keys, values)) 會將鍵列表和值列表配對，快速建立字典
print("\n--- 建立字典 ---")
keys = ["name", "age", "city"]
values = ["John", "30", "NYC"]
d = dict(zip(keys, values))
print(f"dict: {d}")
