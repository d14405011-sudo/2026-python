# R02. 屬性封裝（8.6）
# @property / getter / setter / 唯讀屬性
#
# 本範例重點：
# 1) 使用 @property 把「方法」包裝成「屬性語法」
# 2) 透過 setter 集中做資料驗證，避免非法狀態
# 3) 建立唯讀屬性（只讀不可寫）
# 4) 使用計算型屬性，讓值隨底層資料自動更新

# ── 基本 @property ────────────────────────────────────────
class Circle:
    def __init__(self, radius):
        # 慣例：前綴底線 _radius 表示「內部實作細節」，
        # 外部建議改用公開介面 radius 來讀寫。
        self._radius = radius   # _radius：慣例上表示「受保護」，不直接存取

    @property
    def radius(self):
        # getter：當外部讀取 c.radius 時會呼叫這個方法
        return self._radius

    @radius.setter
    def radius(self, value):
        # setter：當外部指派 c.radius = 新值 時會呼叫這個方法
        # 在這裡統一做驗證，確保物件維持合法狀態。
        if value < 0:
            raise ValueError("半徑不能為負數")
        self._radius = value

    @property
    # area 只有 getter，沒有對應 setter，所以是唯讀屬性。
    # 優點：不需額外儲存 area，每次讀取時即時計算，避免資料不同步。
    def area(self):             # 唯讀屬性（沒有 setter）
        import math
        return math.pi * self._radius ** 2

    @property
    # diameter 同樣是計算型屬性，隨半徑變動自動反映新結果。
    def diameter(self):
        return self._radius * 2


c = Circle(5)
# 讀取屬性時，看起來像資料欄位，實際上會呼叫對應 getter。
print(c.radius)     # 5
print(c.area)       # 78.539...
print(c.diameter)   # 10

c.radius = 10       # 呼叫 setter
print(c.area)       # 314.159...

try:
    # 指派非法值，setter 會丟出 ValueError。
    c.radius = -1   # 觸發 ValueError
except ValueError as e:
    print(e)        # 半徑不能為負數

try:
    # area 沒有 setter，直接賦值會觸發 AttributeError。
    c.area = 100    # 唯讀屬性不能設定
except AttributeError as e:
    print(e)

# ── 用 property 做延遲計算 ────────────────────────────────
class Rectangle:
    def __init__(self, width, height):
        # 這裡直接存公開屬性，重點在展示「計算屬性會自動跟著底層值變化」。
        self.width = width
        self.height = height

    @property
    def area(self):
        # 每次讀取都重新計算，不需手動同步。
        return self.width * self.height

    @property
    def perimeter(self):
        # 周長 = 2 * (寬 + 高)
        return 2 * (self.width + self.height)


r = Rectangle(4, 6)
print(r.area)       # 24
print(r.perimeter)  # 20
r.width = 8         # 修改後 area 自動更新
print(r.area)       # 48
