# R04. 特殊方法（8.2–8.3）
# __eq__ / __lt__ / __len__ / __contains__ / __iter__
#
# 本範例重點：
# 1) 了解「特殊方法（dunder methods）」如何讓自訂類別擁有內建型別般的行為
# 2) 使用 @total_ordering 減少比較運算子的重複實作
# 3) 讓自訂容器支援 len()、in、for 迴圈等 Python 語法糖

from functools import total_ordering

# ── @total_ordering：只需定義 __eq__ 和一個比較方法 ──────
# total_ordering 會根據你提供的 __eq__ + 一個順序比較（如 __lt__），
# 自動補齊 __le__、__gt__、__ge__，降低樣板程式碼。
@total_ordering
class Score:
    def __init__(self, name, value):
        # name：學生名稱（展示用途）
        # value：分數（比較排序依據）
        self.name = name
        self.value = value

    # __repr__ 主要提供給開發者除錯閱讀。
    # {self.name!r} 會用 repr() 顯示字串（含引號），資訊較精確。
    def __repr__(self):
        return f"Score({self.name!r}, {self.value})"

    # __eq__：定義 == 的比較邏輯。
    # 若 other 不是 Score，回傳 NotImplemented 讓 Python 嘗試反向比較或給出合理錯誤。
    # 這比直接回傳 False 更符合 Python 比較協定。
    def __eq__(self, other):
        if not isinstance(other, Score):
            return NotImplemented
        return self.value == other.value

    # __lt__：定義 < 的比較邏輯。
    # 本例以分數 value 作排序依據（不比較 name）。
    def __lt__(self, other):
        if not isinstance(other, Score):
            return NotImplemented
        return self.value < other.value


# 建立三筆分數資料進行比較示範
s1 = Score("Alice", 90)
s2 = Score("Bob", 75)
s3 = Score("Carol", 90)

# s1 > s2 會由 total_ordering 與 __lt__/__eq__ 推導出結果
print(s1 > s2)      # True  （由 __lt__ 推導）
print(s1 == s3)     # True
print(s1 != s2)     # True  （由 __eq__ 推導）
# sorted() 需要可比較性；此處可依分數升冪排列
print(sorted([s1, s2, s3]))     # 升冪排列

# ── __len__ / __contains__ / __iter__ ────────────────────
# 這個類別示範「自訂容器」的行為：
# - __len__      → 支援 len(obj)
# - __contains__ → 支援 x in obj
# - __iter__     → 支援 for ... in obj
class Classroom:
    def __init__(self, name):
        self.name = name
        # 內部實際資料結構使用 list 儲存學生名單
        self._students = []

    def add(self, student):
        # 新增學生到名單尾端
        self._students.append(student)

    def __len__(self):
        # 當呼叫 len(cls) 時會執行此方法
        return len(self._students)

    def __contains__(self, student):
        # 當使用 student in cls 時會執行此方法
        return student in self._students

    def __iter__(self):
        # 回傳可迭代器，讓 for 迴圈能逐一取出學生
        return iter(self._students)

    def __repr__(self):
        # 這裡直接呼叫 len(self)，實際上會觸發 __len__
        return f"Classroom({self.name!r}, {len(self)} 人)"


# 建立一個教室並加入三位學生
cls = Classroom("資工一甲")
cls.add("Alice")
cls.add("Bob")
cls.add("Carol")

# len() / in / for 都會分別觸發對應特殊方法
print(len(cls))             # 3
print("Alice" in cls)       # True
print("Dave" in cls)        # False

for student in cls:         # __iter__ 讓 for 迴圈可用
    print(student)
