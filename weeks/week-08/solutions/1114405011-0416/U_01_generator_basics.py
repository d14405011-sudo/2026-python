# Understand（理解）- 生成器概念
# =====================================
# 生成器是一種特殊的函數，使用 yield 關鍵字，每次執行會暫停在 yield 處並返回值
# 優點：節省記憶體（延遲執行）、可以生成無限序列、代碼更簡潔
# 常見應用：大文件讀取、無限數列生成、樹/圖遍歷、鏈式操作

# 示例 1：自定義 frange 函數（浮點數範圍生成器）
# range() 不支援浮點數步長，使用 yield 可以模擬實現
def frange(start, stop, step):
    """生成從 start 到 stop 的浮點數序列，步長為 step"""
    if step == 0:
        raise ValueError("step must not be zero")

    x = start
    if step > 0:
        while x < stop:
            yield x  # 暫停執行，返回當前值 x，下次呼叫 next() 會從這裡繼續
            x += step
    else:
        while x > stop:
            yield x  # 暫停執行，返回當前值 x，下次呼叫 next() 會從這裡繼續
            x += step

result = list(frange(0, 2, 0.5))
print(f"frange(0, 2, 0.5): {result}")

# 示例 2：countdown 生成器 - 演示生成器的執行流程
# 每次 yield 時函數會暫停，print(「Done!」) 只在生成器全部消耗後才執行
def countdown(n):
    """從 n 倒數到 1 的生成器"""
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n  # 暫停並返回 n
        n -= 1
    print("Done!")

# 演示 countdown 生成器的行為
print("\n--- 建立生成器 ---")
c = countdown(3)
print(f"生成器物件: {c}")  # 生成器物件本身沒有開始執行

print("\n--- 逐步迭代 ---")
# 第一次呼叫 next() 會執行至第一個 yield，返回 3
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")
# 當生成器用盡時，會拋出 StopIteration 例外

try:
    next(c)  # 這會拋出 StopIteration（生成器已結束）
except StopIteration:
    print("StopIteration!")


# 示例 3：無限生成器 - Fibonacci 數列
# while True 表示這個生成器可以無限運行（除非主動停止）
def fibonacci():
    """無限產生 Fibonacci 數列"""
    a, b = 0, 1
    while True:
        yield a  # 每次返回當前的 a 值
        a, b = b, a + b  # 更新 a 和 b


print("\n--- Fibonacci 生成器 ---")
fib = fibonacci()
# 使用 range(10) 限制只取前 10 個值，否則會無限執行
for i in range(10):
    print(next(fib), end=" ")
print()


# 示例 4：yield from - 委派給子生成器
# yield from 用來簡化「將子生成器的所有值逐一 yield」的行為
def chain_iter(*iterables):
    """將多個可迭代物件連接起來"""
    for it in iterables:
        # yield from it 相等於：for x in it: yield x
        yield from it


print("\n--- yield from 用法 ---")
result = list(chain_iter([1, 2], [3, 4], [5, 6]))
print(f"chain_iter: {result}")


# 示例 5：樹的深度優先遍歷 - 生成器在遞歸中的應用
class Node:
    """樹的節點類"""
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        """添加子節點"""
        self.children.append(node)

    def __iter__(self):
        """使此節點可迭代（返回子節點）"""
        return iter(self.children)

    def depth_first(self):
        """深度優先遍歷 - yield 自己，然後遞歸 yield 所有後代"""
        yield self  # 先 yield 當前節點
        for child in self:
            # yield from 會委派給子樹的 depth_first()，逐一yield 所有後代
            yield from child.depth_first()


print("\n--- 樹的深度優先遍歷 ---")
# 建立一個樹：
#       0
#      / \
#     1   2
#    / \
#   3   4
root = Node(0)
root.add_child(Node(1))
root.add_child(Node(2))
root.children[0].add_child(Node(3))
root.children[0].add_child(Node(4))

# 深度優先訪問順序：0 -> 1 -> 3 -> 4 -> 2
for node in root.depth_first():
    print(node.value, end=" ")
print()


# 示例 6：巢狀序列攤平 - 遞歸生成器應用
def flatten(items):
    """遞歸地攤平巢狀序列"""
    for x in items:
        # 檢查 x 是否可迭代且不是字串（字串也可迭代但我們不想拆它）
        if hasattr(x, "__iter__") and not isinstance(x, str):
            # 遞歸呼叫 flatten，並用 yield from 逐一 yield 結果
            yield from flatten(x)
        else:
            # 不可迭代或是字串，直接 yield
            yield x


print("\n--- 巢狀序列攤平 ---")
nested = [1, [2, [3, 4]], 5]
print(f"展開: {list(flatten(nested))}")
