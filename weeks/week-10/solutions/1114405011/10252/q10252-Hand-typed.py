from __future__ import annotations

from typing import List, Tuple


def one_axis(values: List[int]) -> Tuple[int, int]:
    values.sort()
    n = len(values)
    l = values[(n - 1) // 2]
    r = values[n // 2]
    s = sum(abs(v - l) for v in values)
    c = r - l + 1
    return s, c


def solve(raw: str) -> str:
    arr = list(map(int, raw.strip().split()))
    p = 0
    t = arr[p]
    p += 1
    out = []

    for _ in range(t):
        n = arr[p]
        p += 1
        xs, ys = [], []
        for _ in range(n):
            x, y = arr[p], arr[p + 1]
            p += 2
            xs.append(x)
            ys.append(y)
        sx, cx = one_axis(xs)
        sy, cy = one_axis(ys)
        out.append(f"{sx + sy} {cx * cy}")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
