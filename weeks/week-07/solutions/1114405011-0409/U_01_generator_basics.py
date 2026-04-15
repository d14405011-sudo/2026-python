# Understand（理解）- 生成器概念
#
# 本檔案重點：
# 1) 使用 yield 建立「惰性計算」的序列
# 2) 生成器在 next() 之間如何保留狀態
# 3) yield from 的委派機制
# 4) 生成器在實務上的遞迴走訪與攤平應用


def frange(start, stop, step):
    # 類似 range，但支援浮點步進
    # 每次 yield 一個值，避免一次建立完整列表（省記憶體）
    x = start
    while x < stop:
        yield x
        x += step


result = list(frange(0, 2, 0.5))
print(f"frange(0, 2, 0.5): {result}")


def countdown(n):
    # 觀察點：這段 print 不會在「定義函式」時執行，
    # 而是在第一次 next() 啟動生成器時才執行
    print(f"Starting countdown from {n}")
    while n > 0:
        # 每次 yield 後，函式會暫停在這一行，
        # 下一次 next() 再從這裡繼續
        yield n
        n -= 1
    print("Done!")


print("\n--- 建立生成器 ---")
c = countdown(3)
# 此時只建立了 generator 物件，函式主體尚未開始跑
print(f"生成器物件: {c}")

print("\n--- 逐步迭代 ---")
# 逐次 next() 可清楚看出生成器的狀態推進
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")

try:
    # 第四次再取值會觸發 StopIteration（序列結束）
    next(c)
except StopIteration:
    print("StopIteration!")


def fibonacci():
    # 無窮序列範例：只要持續 next() 就能一直產生下一個費氏數
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("\n--- Fibonacci 生成器 ---")
fib = fibonacci()
for i in range(10):
    print(next(fib), end=" ")
print()


def chain_iter(*iterables):
    # yield from 可把「子迭代器」的元素直接往外轉交
    # 等價於：for x in it: yield x
    for it in iterables:
        yield from it


print("\n--- yield from 用法 ---")
result = list(chain_iter([1, 2], [3, 4], [5, 6]))
print(f"chain_iter: {result}")


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __iter__(self):
        # 讓 Node 可被 for 走訪其子節點
        return iter(self.children)

    def depth_first(self):
        # 前序深度優先：先回傳自己，再遞迴子樹
        yield self
        for child in self:
            yield from child.depth_first()


print("\n--- 樹的深度優先遍歷 ---")
root = Node(0)
root.add_child(Node(1))
root.add_child(Node(2))
root.children[0].add_child(Node(3))
root.children[0].add_child(Node(4))

for node in root.depth_first():
    print(node.value, end=" ")
print()


def flatten(items):
    # 遞迴攤平任意巢狀可迭代結構（排除字串，避免被拆成字元）
    for x in items:
        if hasattr(x, "__iter__") and not isinstance(x, str):
            yield from flatten(x)
        else:
            yield x


print("\n--- 巢狀序列攤平 ---")
nested = [1, [2, [3, 4]], 5]
print(f"展開: {list(flatten(nested))}")
