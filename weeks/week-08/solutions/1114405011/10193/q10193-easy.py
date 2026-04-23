"""
UVA 10193 - easy 版

易記版本：
- 二進位轉十進位。
- 用 gcd 判斷是否大於 1。
"""

import math


def solve_case(a_bin: str, b_bin: str, idx: int) -> str:
    a = int(a_bin, 2)
    b = int(b_bin, 2)
    ok = math.gcd(a, b) > 1
    if ok:
        return f"Pair #{idx}: All you need is love!"
    return f"Pair #{idx}: Love is not all you need!"


def solve_all(text: str) -> str:
    arr = [s.strip() for s in text.splitlines() if s.strip()]
    if not arr:
        return ""
    t = int(arr[0])
    out = []
    j = 1
    for i in range(1, t + 1):
        out.append(solve_case(arr[j], arr[j + 1], i))
        j += 2
    return "\n".join(out)


def main() -> None:
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
