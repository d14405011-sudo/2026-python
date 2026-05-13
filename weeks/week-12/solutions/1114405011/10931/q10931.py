"""UVA 10931 - Parity

標準版解法：
- 直接使用 Python 轉二進位能力。
- 再統計 1 的個數作為 parity。
"""

from __future__ import annotations


def parity_info(value: int) -> tuple[str, int]:
    """回傳二進位字串與 1 的個數。"""
    b = bin(value)[2:]
    ones = b.count("1")
    return b, ones


def format_line(value: int) -> str:
    """依題目指定格式輸出單行字串。"""
    b, p = parity_info(value)
    return f"The parity of {b} is {p} (mod 2)."


def solve_all(text: str) -> str:
    """逐行處理輸入，遇到 0 結束。"""
    out: list[str] = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue

        v = int(s)
        if v == 0:
            break

        out.append(format_line(v))

    return "\n".join(out)


def main() -> None:
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
