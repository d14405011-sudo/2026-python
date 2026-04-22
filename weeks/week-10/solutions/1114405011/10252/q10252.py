"""
題號 10252 一般版解法

此題可視為在整數平面上找點 P=(a,b)，使
sum(|xi-a| + |yi-b|) 最小，並輸出：
1) 最小距離和
2) 能達成最小值的整數解個數

關鍵性質（曼哈頓距離）：
- x 與 y 可分開獨立最小化。
- 一維情況最小值出現在中位數區間。
  - n 為奇數：中位數唯一
  - n 為偶數：介於中間兩值之間所有整數都同為最小
"""

from __future__ import annotations

from typing import List, Tuple


def one_dim_min_and_count(vals: List[int]) -> Tuple[int, int]:
    """回傳一維最小距離和，以及能達到最小值的整數點個數。"""
    vals = sorted(vals)
    n = len(vals)

    lo = vals[(n - 1) // 2]
    hi = vals[n // 2]

    # 在 [lo, hi] 區間內任取整數都可達最小值；取 lo 來計算最小和即可
    min_sum = sum(abs(v - lo) for v in vals)
    count = hi - lo + 1
    return min_sum, count


def solve(raw: str) -> str:
    it = iter(raw.strip().split())
    t = int(next(it))
    out: List[str] = []

    for _ in range(t):
        n = int(next(it))
        xs: List[int] = []
        ys: List[int] = []
        for _ in range(n):
            x = int(next(it))
            y = int(next(it))
            xs.append(x)
            ys.append(y)

        sx, cx = one_dim_min_and_count(xs)
        sy, cy = one_dim_min_and_count(ys)
        out.append(f"{sx + sy} {cx * cy}")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print(solve(data), end="")
