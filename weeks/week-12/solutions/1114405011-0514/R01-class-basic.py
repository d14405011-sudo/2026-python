# R01. 類別基礎（8.1）
# __init__ / 方法 / __repr__ / __str__
#
# 本範例重點：
# 1) 如何定義 class 與建立物件（instance）
# 2) __init__、__repr__、__str__ 的用途與差異
# 3) 實例方法中 self 的意義
# 4) 類別變數（class variable）與實例變數（instance variable）差別

# ── 最簡單的 class ────────────────────────────────────────
class Point:
    # __init__ 是建構子（initializer），在建立物件時自動呼叫。
    # Point(0, 0) 其實會先建立物件，再呼叫 __init__(self, 0, 0)。
    def __init__(self, x, y):
        # self 代表「目前這個物件本身」。
        # 將外部傳入的 x、y 存成物件屬性。
        self.x = x
        self.y = y

    # __repr__：給開發者看，eval() 能重建物件最理想
    # 當你在互動式環境直接輸入物件名稱、或用 repr(obj) 時會呼叫。
    # 目標是「明確、可除錯」。
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    # __str__：給使用者看，print() 時呼叫
    # 當用 print(obj) 或 str(obj) 時優先呼叫 __str__。
    # 目標是「可讀、友善」。
    def __str__(self):
        return f"({self.x}, {self.y})"

    # 實例方法：計算目前點（self）到另一點（other）的歐氏距離。
    # 公式：sqrt((x1-x2)^2 + (y1-y2)^2)
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# 建立兩個 Point 物件
p1 = Point(0, 0)
p2 = Point(3, 4)

# repr(p1) 呼叫 __repr__，偏向開發除錯用途
print(repr(p1))             # Point(0, 0)
# str(p2) 呼叫 __str__，偏向使用者顯示用途
print(str(p2))              # (3, 4)
# 距離為 3-4-5 直角三角形，結果應為 5.0
print(p1.distance_to(p2))  # 5.0

# ── 類別變數 vs 實例變數 ──────────────────────────────────
class Student:
    school = "國立澎湖科技大學"    # 類別變數：所有實例共用

    def __init__(self, name, student_id):
        # 下面兩個是實例變數：每個物件各自擁有，不互相影響。
        self.name = name            # 實例變數：每個實例獨立
        self.student_id = student_id

    def __repr__(self):
        return f"Student({self.student_id}, {self.name})"

    # 實例方法中可直接透過 self.school 存取類別變數。
    # 若該實例沒有同名屬性，Python 會往 class 找 school。
    def greeting(self):
        return f"我是 {self.school} 的 {self.name}"


# 建立兩位學生實例
s1 = Student("王小明", "11144050001")
s2 = Student("李小華", "11144050002")

print(s1.greeting())
print(s2.school)            # 透過實例存取類別變數
print(Student.school)       # 透過類別名稱存取

# 修改類別變數影響所有實例
# 因為 school 是 class 層級共用資料，改一次所有實例都會看到新值。
Student.school = "NPU"
print(s1.school)            # NPU
print(s2.school)            # NPU
