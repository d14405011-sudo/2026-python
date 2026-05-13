"""UVA 10929 - Multiple of 11

標準版解法：
- 以逐位取餘數的方式判斷是否為 11 的倍數。
- 可處理上千位數字，不需轉成大整數。
"""

from __future__ import annotations


def is_multiple_of_11(num_text: str) -> bool:
    """以字串方式計算 num_text 是否為 11 的倍數。"""
    remainder = 0
    for ch in num_text:
        remainder = (remainder * 10 + (ord(ch) - ord("0"))) % 11
    return remainder == 0


def format_line(num_text: str) -> str:
    """依題目格式產生輸出行。"""
    if is_multiple_of_11(num_text):
        return f"{num_text} is a multiple of 11."
    return f"{num_text} is not a multiple of 11."


def solve_all(text: str) -> str:
    """逐行處理，遇到 0 停止。"""
    out: list[str] = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s == "0":
            break
        out.append(format_line(s))
    return "\n".join(out)


def main() -> None:
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
