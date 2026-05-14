"""UVA 10922 - 2 the 9s

標準版解法：
- 先以字串處理大整數，避免溢位。
- 透過反覆「位數和」求 9-degree。
"""

from __future__ import annotations

from typing import Optional


def digit_sum(num_text: str) -> int:
    """回傳字串數字的位數總和。"""
    return sum(ord(ch) - ord("0") for ch in num_text)


def nine_degree(num_text: str) -> Optional[int]:
    """若為 9 的倍數，回傳 9-degree；否則回傳 None。"""
    # 9 本身是 9 的倍數，且深度定義為 1。
    if num_text == "9":
        return 1

    first_sum = digit_sum(num_text)
    if first_sum % 9 != 0:
        return None

    # 對於非 "9" 的輸入，從原字串做第一次位數和這一步
    # 也必須計入 9-degree；例如 "18" -> 9，degree 應為 2。
    degree = 2
    current = first_sum

    # 持續把數字做位數和，直到成為單一位數。
    while current > 9:
        current = digit_sum(str(current))
        degree += 1

    return degree if current == 9 else None


def format_line(num_text: str) -> str:
    """依題目格式輸出單一數字的判斷結果。"""
    deg = nine_degree(num_text)
    if deg is None:
        return f"{num_text} is not a multiple of 9."
    return f"9-degree of {num_text} is {deg}."


def solve_all(text: str) -> str:
    """處理多行輸入，遇到 0 結束。"""
    out: list[str] = []
    for raw in text.splitlines():
        n = raw.strip()
        if not n:
            continue
        if n == "0":
            break
        out.append(format_line(n))
    return "\n".join(out)


def main() -> None:
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
