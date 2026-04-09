# Remember（記憶）- 迭代器基礎概念
#
# 本檔案重點：
# 1) 什麼是「可迭代物件（iterable）」與「迭代器（iterator）」
# 2) iter() / next() 與 StopIteration 的關係
# 3) 如何自訂可迭代類別與迭代器類別
# 4) 手動模擬 for 迴圈的迭代流程

# 1. 迭代器協議的核心方法
items = [1, 2, 3]

# iter() 會對 iterable 呼叫 __iter__()，取得「迭代器物件」
it = iter(items)
print(f"迭代器: {it}")

# next() 會對 iterator 呼叫 __next__()，每次取出一個元素
print(f"第一個: {next(it)}")  # 1
print(f"第二個: {next(it)}")  # 2
print(f"第三個: {next(it)}")  # 3

# 當沒有更多元素時，__next__() 必須拋出 StopIteration
# for 迴圈會自動處理這個例外；手動 next() 則要自行捕捉
try:
    next(it)
except StopIteration:
    print("迭代結束!")

# 2. 常見可迭代物件
print("\n--- 常見可迭代物件 ---")

# 列表：可迭代（iterable）
print(f"列表 iter: {iter([1, 2, 3])}")

# 字串：可逐字元迭代
print(f"字串 iter: {iter('abc')}")

# 字典：預設迭代的是 key
print(f"字典 iter: {iter({'a': 1, 'b': 2})}")

# 檔案物件：逐行迭代
import io

f = io.StringIO("line1\nline2\nline3")
print(f"檔案 iter: {iter(f)}")


# 3. 自訂可迭代物件
class CountDown:
    # 可迭代容器：負責回傳一個新的迭代器
    # 這樣每次 for 重新迭代時，都能從初始值重新開始
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return CountDownIterator(self.start)


class CountDownIterator:
    # 迭代器：維護「目前狀態（current）」並實作 __next__
    def __init__(self, start):
        self.current = start

    def __next__(self):
        # 終止條件：當 current <= 0，表示沒有下一個值
        if self.current <= 0:
            raise StopIteration

        # 回傳目前值後往下遞減
        self.current -= 1
        return self.current + 1


print("\n--- 自訂迭代器 ---")
for i in CountDown(3):
    print(i, end=" ")  # 3 2 1

# 4. 迭代器 vs 可迭代物件
print("\n\n--- 迭代器 vs 可迭代物件 ---")

# 列表只有 __iter__，沒有 __next__，因此是 iterable 不是 iterator
my_list = [1, 2, 3]
print(f"列表: 可迭代物件 ✓, 迭代器 ✗")

# 對列表呼叫 iter() 會得到 list_iterator（真正可 next() 的物件）
my_iter = iter(my_list)
print(f"iter(列表): 可迭代物件 ✗, 迭代器 ✓")

# 迭代器通常同時具備：
# - __iter__（且通常回傳 self）
# - __next__（提供下一個值）
print(f"迭代器: 可迭代物件 ✓ (有__iter__), 迭代器 ✓ (有__next__)")

# 5. StopIteration 例外
print("\n--- StopIteration 用法 ---")


# 手動遍歷（章節 4.1 風格）
# 等價於 for item in items: ... 的核心機制
def manual_iter(items):
    it = iter(items)
    while True:
        try:
            item = next(it)
            print(f"取得: {item}")
        except StopIteration:
            # 捕捉到 StopIteration 代表資料耗盡
            break


manual_iter(["a", "b", "c"])


# 使用 next(iterator, default) 的版本
# 注意：若資料中真的可能出現 None，應改用專屬 sentinel 物件避免誤判
def manual_iter_default(items):
    it = iter(items)
    while True:
        item = next(it, None)  # 預設值
        if item is None:
            break
        print(f"取得: {item}")


print("\n使用預設值:")
manual_iter_default(["a", "b", "c"])
