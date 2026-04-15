"""
UVA 10221 - easy 版

易記版三步：
1. 先轉角度（min -> deg）。
2. 角度若大於 180，改用 360-a。
3. 套弧長/弦長公式。
"""

import math


def solve_line(s: float, a: float, unit: str) -> str:
    if unit == "min":
        a = a / 60.0
    if a > 180.0:
        a = 360.0 - a

    r = 6440.0 + s
    t = math.radians(a)
    arc = r * t
    chord = 2.0 * r * math.sin(t / 2.0)
    return f"{arc:.6f} {chord:.6f}"


def solve_all(text: str) -> str:
    rows = []
    for s in text.splitlines():
        s = s.strip()
        if not s:
            continue
        x, y, u = s.split()
        rows.append(solve_line(float(x), float(y), u))
    return "\n".join(rows)


def main() -> None:
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
