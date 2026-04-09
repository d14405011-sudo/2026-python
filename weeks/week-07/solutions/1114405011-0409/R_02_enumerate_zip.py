# Remember（記憶）- enumerate() 和 zip()
#
# 本檔案重點：
# 1) enumerate()：在迭代時同時取得索引與值
# 2) zip()：把多個序列「對齊配對」後一起走訪
# 3) zip_longest()：長度不一致時補齊資料

colors = ["red", "green", "blue"]

print("--- enumerate() 基本用法 ---")
# enumerate(sequence) 會回傳 (index, value) 的 iterator
for i, color in enumerate(colors):
    print(f"{i}: {color}")

print("\n--- enumerate(start=1) ---")
# start=1 常用在「人類可讀編號」(第 1 個、第 2 個...)
for i, color in enumerate(colors, 1):
    print(f"第{i}個: {color}")

print("\n--- enumerate with 檔案 ---")
lines = ["line1", "line2", "line3"]
# 真正讀檔時也常搭配 enumerate(file, 1) 產生行號
for lineno, line in enumerate(lines, 1):
    print(f"行 {lineno}: {line}")

print("\n--- zip() 基本用法 ---")
names = ["Alice", "Bob", "Carol"]
scores = [90, 85, 92]
# zip(names, scores) -> (name, score) 成對輸出
for name, score in zip(names, scores):
    print(f"{name}: {score}")

print("\n--- zip() 多個序列 ---")
a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]
# zip 可同時綁 3 個以上序列
for x, y, z in zip(a, b, c):
    print(f"{x} + {y} + {z} = {x + y + z}")

print("\n--- zip() 長度不同 ---")
x = [1, 2]
y = ["a", "b", "c"]
# 預設 zip 會以「最短序列」為準，多餘元素直接忽略
print(f"list(zip(x, y)): {list(zip(x, y))}")

from itertools import zip_longest

# zip_longest 以最長序列為準，缺值用 fillvalue 補
print(f"zip_longest: {list(zip_longest(x, y, fillvalue=0))}")

print("\n--- 建立字典 ---")
keys = ["name", "age", "city"]
values = ["John", "30", "NYC"]
# dict(zip(keys, values)) 是常見鍵值配對寫法
d = dict(zip(keys, values))
print(f"dict: {d}")
