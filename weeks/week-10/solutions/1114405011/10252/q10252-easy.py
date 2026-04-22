"""
題號 10252 -easy 版

最好背的版本：
- 曼哈頓距離可拆成 x 與 y 兩題一維問題。
- 一維時最小值在中位數區間。
- 偶數個點會有一段平坦區間，因此可能有多個整數最佳解。
"""

from __future__ import annotations

from typing import List, Tuple


def one_axis(values: List[int]) -> Tuple[int, int]:
    values.sort()
    n = len(values)

    left_mid = values[(n - 1) // 2]
    right_mid = values[n // 2]

    # 取中位數區間任一點都可達最小值，這裡用 left_mid 計算最小距離和
    best_sum = sum(abs(v - left_mid) for v in values)
    count = right_mid - left_mid + 1
    return best_sum, count


def solve(raw: str) -> str:
    nums = list(map(int, raw.strip().split()))
    ptr = 0
    t = nums[ptr]
    ptr += 1

    out: List[str] = []
    for _ in range(t):
        n = nums[ptr]
        ptr += 1

        xs: List[int] = []
        ys: List[int] = []
        for _ in range(n):
            x = nums[ptr]
            y = nums[ptr + 1]
            ptr += 2
            xs.append(x)
            ys.append(y)

        sx, cx = one_axis(xs)
        sy, cy = one_axis(ys)
        out.append(f"{sx + sy} {cx * cy}")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
