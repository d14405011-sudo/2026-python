# R03. 繼承與 super()（8.7）
# 繼承 / 方法覆寫 / super() / isinstance / issubclass
#
# 本範例重點：
# 1) 以基底類別（Animal）定義共同行為
# 2) 子類別（Dog / Cat）覆寫同名方法（speak）
# 3) 使用 super() 重用父類別初始化與方法
# 4) 理解 isinstance / issubclass 的型別判斷
# 5) 透過多型（Polymorphism）統一呼叫介面

# ── 基底類別 ─────────────────────────────────────────────
class Animal:
    # 所有動物都至少有 name，放在基底類別統一管理。
    def __init__(self, name):
        self.name = name

    # 預設行為：子類別可沿用，也可覆寫。
    def speak(self):
        return f"{self.name} 發出聲音"

    # __repr__ 用於開發除錯；
    # __class__.__name__ 可自動顯示實際類別名稱（Animal / Dog / Cat...）。
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"


# ── 子類別：覆寫方法 ──────────────────────────────────────
# Dog 繼承 Animal，但提供自己的 speak() 實作。
class Dog(Animal):
    def speak(self):
        return f"{self.name} 說：汪汪！"


# Cat 同樣繼承 Animal，覆寫成貓叫聲。
class Cat(Animal):
    def speak(self):
        return f"{self.name} 說：喵～"


# ── super()：呼叫父類別方法 ───────────────────────────────
# GuideDog 繼承 Dog（間接也繼承 Animal）。
class GuideDog(Dog):
    def __init__(self, name, owner):
        # super().__init__(name) 會沿著 MRO 呼叫父類別初始化。
        # 此處 Dog 沒有自訂 __init__，因此最終使用 Animal.__init__。
        super().__init__(name)      # 呼叫 Dog → Animal 的 __init__
        self.owner = owner

    def speak(self):
        # 先重用 Dog 的 speak()，再附加導盲犬額外資訊。
        base = super().speak()      # 呼叫 Dog.speak()
        return f"{base}（導盲犬，主人：{self.owner}）"


# 建立三種不同型別的物件（但都屬於 Animal 家族）
d = Dog("小黑")
c = Cat("咪咪")
g = GuideDog("阿金", "王伯伯")

# 同一段迴圈中，呼叫相同方法名稱 speak()，
# 會依物件的「實際型別」執行對應版本（動態派發）。
for animal in [d, c, g]:
    print(animal.speak())

# ── isinstance / issubclass ───────────────────────────────
# isinstance(obj, Class)：判斷「物件是否為某類別或其子類別實例」
print(isinstance(d, Dog))       # True
print(isinstance(d, Animal))    # True（Dog 是 Animal 的子類別）
print(isinstance(d, Cat))       # False

# issubclass(Sub, Base)：判斷「類別是否為另一類別的子類別」
print(issubclass(Dog, Animal))  # True
print(issubclass(Cat, Dog))     # False

# ── 多型（Polymorphism）──────────────────────────────────
# 只要物件有 speak()，此函式就能運作，不需分別寫 Dog/Cat/GuideDog 版本。
# 這就是多型帶來的擴充性：新增新動物類別時，此函式通常不需改。
def make_sounds(animals: list):
    for a in animals:
        print(a.speak())        # 各自呼叫自己的 speak()

make_sounds([d, c, g])
