"""Q10055 簡化版本 - 適合考試"""

def solve():
    n, q = map(int, input().split())

    # Fenwick Tree (Binary Indexed Tree) for flip counts
    bit = [0] * (n + 2)

    def update(i: int, delta: int) -> None:
        """Add delta to position i in BIT."""
        while i <= n:
            bit[i] += delta
            i += i & -i

    def prefix_sum(i: int) -> int:
        """Return sum of values in [1..i]."""
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    for _ in range(q):
        op = list(map(int, input().split()))
        if op[0] == 1:
            # 翻轉操作：記錄此位置被翻轉一次
            idx = op[1]
            update(idx, 1)
        else:
            # 查詢操作：區間內減函數個數的奇偶性
            l, r = op[1], op[2]
            total_flips = prefix_sum(r) - prefix_sum(l - 1)
            print(total_flips % 2)

solve()
