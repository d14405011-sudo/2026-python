"""UVA 10922 - 2 the 9s（好記版）

記憶流程：
1. 先看是不是 9 的倍數
2. 是的話一直做位數和
3. 數到變成 9 的次數就是 9-degree
"""

from __future__ import annotations


def sum_digits_easy(s: str) -> int:
    """簡單位數和函式。"""
    return sum(int(ch) for ch in s)


def nine_degree_easy(s: str):
    """回傳 9-degree，不是 9 倍數就回傳 None。"""
    if s == "9":
        return 1

    x = sum_digits_easy(s)
    if x % 9 != 0:
        return None

    degree = 1
    while x > 9:
        x = sum_digits_easy(str(x))
        degree += 1

    if x == 9:
        return degree
    return None


def solve_all_easy(text: str) -> str:
    """逐行處理，0 為終止輸入。"""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s == "0":
            break
        d = nine_degree_easy(s)
        if d is None:
            out.append(f"{s} is not a multiple of 9.")
        else:
            out.append(f"9-degree of {s} is {d}.")
    return "\n".join(out)


def main() -> None:
    import sys

    src = sys.stdin.read()
    res = solve_all_easy(src)
    if res:
        print(res)


if __name__ == "__main__":
    main()
