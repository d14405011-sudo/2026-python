# R02. 物件特殊方法
# 讓自訂的 class 表現得像 Python 內建型別（可比較、可列印、可排序...）
# 對應 Bloom's Taxonomy：記憶（Remember）— 背得出哪個場景用哪個方法

# ── __repr__ 和 __str__：物件的自我介紹 ──────────────────
# __repr__：給「開發者」看的（在 REPL、debug、log 時出現，盡量能重現物件）
# __str__ ：給「使用者」看的（print()、str() 優先用這個，重視可讀性）


# 定義一個學生類別，示範 __repr__ 與 __str__ 差異
class Student:
    def __init__(self, name, grade):
        self.name = name  # 學生姓名
        self.grade = grade  # 分數

    def __repr__(self):
        # 盡量寫成能重建物件的格式
        return f"Student(name={self.name!r}, grade={self.grade})"

    def __str__(self):
        # 只顯示給使用者看的簡潔資訊
        return f"{self.name}：{self.grade} 分"


print("=== __repr__ vs __str__ ===")
s = Student("王小明", 85)
print(repr(s))   # 直接顯示物件完整資訊，方便 debug
print(str(s))    # 只顯示友善資訊，給一般使用者
print(s)         # print() 會自動用 __str__

# ── __eq__：自訂「相等」的意義 ────────────────────────────
# 沒有 __eq__ 的話，兩個物件只有「同一個記憶體位置」才算相等


# 定義一個點的類別，示範自訂 __eq__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        # 先檢查型別，避免亂比
        if not isinstance(other, Point):
            return NotImplemented
        # 只要座標一樣就算相等
        return self.x == other.x and self.y == other.y


print("\n=== __eq__：自訂相等條件 ===")
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)
print(p1 == p2)  # True，雖然是不同物件，但座標一樣
print(p1 == p3)  # False，座標不同
print(p1 is p2)  # False，is 比較的是記憶體位置

# ── @total_ordering：自動補齊所有比較運算子 ─────────────
# 只要定義 __eq__ 和一個比較（__lt__），
# @total_ordering 會自動補出 <=, >, >= 四個


# @total_ordering 幫你自動補齊所有比較運算子
from functools import total_ordering

@total_ordering
class Score:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Score({self.value})"

    def __eq__(self, other):
        # 先檢查型別，避免與非 Score 物件比較時出錯
        if not isinstance(other, Score):
            return NotImplemented
        # 只要分數一樣就算相等
        return self.value == other.value

    def __lt__(self, other):
        # 先檢查型別，避免與非 Score 物件比較時出錯
        if not isinstance(other, Score):
            return NotImplemented
        # 分數小於對方
        return self.value < other.value

scores = [Score(70), Score(95), Score(60)]

print("\n=== @total_ordering：只寫兩個，自動補齊全部 ===")
a = Score(80)
b = Score(90)
print(a < b)   # True，直接用 __lt__
print(a > b)   # False，自動補出 __gt__
print(a <= b)  # True，自動補出 __le__

scores = [Score(70), Score(95), Score(60)]
print(sorted(scores))  # 會自動用 __lt__ 排序

# ── __slots__：大量物件時節省記憶體 ──────────────────────
# 一般 class 每個物件都有一個 __dict__，很耗記憶體
# CPE 題目有時會建立幾十萬個小物件，__slots__ 可以大幅節省


# __slots__ 限定物件只能有特定屬性，省下 __dict__ 記憶體空間
class PointLite:
    __slots__ = ('x', 'y')   # 只能有 x, y 兩個屬性，不能動態新增

    def __init__(self, x, y):
        self.x = x
        self.y = y


print("\n=== __slots__：固定屬性，節省記憶體 ===")
p = PointLite(3, 4)
print(p.x, p.y)   # 3 4
# p.z = 5  # 這行會 AttributeError，因為 z 不在 __slots__ 裡，不能動態加屬性

# 記憶重點 ──────────────────────────────────────────────────
# __repr__  → 開發者用，要能「重現」物件，方便 debug
# __str__   → 使用者用，print() 呼叫，重視可讀性
# __eq__    → 自訂 == 的意義，讓物件可比內容
# @total_ordering + __lt__ → 只要寫 __eq__ 和 __lt__，其餘比較自動補齊
# __slots__ → 固定屬性，大量物件時省記憶體，不能動態加屬性
