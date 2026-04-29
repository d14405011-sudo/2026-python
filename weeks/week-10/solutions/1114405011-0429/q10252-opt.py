"""
題號 10252 -opt 版（優化）

相較 easy 版的改進：
1. one_axis 改用前綴和（prefix sum），將中位數成本計算
   從逐元素 sum(abs(v - mid) for v in values)（O(n) 乘法）
   改為 O(1) 算術公式，常數項更小：
     left_cost  = (lo+1)*mid - prefix[lo+1]
     right_cost = (prefix[n] - prefix[lo+1]) - (n-lo-1)*mid
2. 輸入改用逐 token 迭代器（iter + next），
   避免預先建立完整整數列表，節省一次 map+list 分配。
"""

from __future__ import annotations

from typing import List, Tuple


def one_axis(values: List[int]) -> Tuple[int, int]:
    values.sort()
    n = len(values)

    # 前綴和
    prefix = [0] * (n + 1)
    for i, v in enumerate(values):
        prefix[i + 1] = prefix[i] + v

    lo = (n - 1) // 2
    hi = n // 2
    m = values[lo]

    # sum|v - m| 分左右兩段 O(1) 計算
    left_cost  = (lo + 1) * m - prefix[lo + 1]
    right_cost = (prefix[n] - prefix[lo + 1]) - (n - lo - 1) * m
    best_sum   = left_cost + right_cost
    count      = values[hi] - m + 1

    return best_sum, count


def solve(raw: str) -> str:
    it = iter(raw.split())
    t = int(next(it))
    out: List[str] = []

    for _ in range(t):
        n = int(next(it))
        xs: List[int] = []
        ys: List[int] = []
        for _ in range(n):
            xs.append(int(next(it)))
            ys.append(int(next(it)))

        sx, cx = one_axis(xs)
        sy, cy = one_axis(ys)
        out.append(f"{sx + sy} {cx * cy}")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
