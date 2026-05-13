"""UVA 10931 - Parity（好記版）

好記流程：
1. 除 2 取餘拿到每個 bit
2. 反轉得到二進位字串
3. 數 1 的數量
"""

from __future__ import annotations


def to_binary_and_ones_easy(n: int) -> tuple[str, int]:
    """手動把十進位轉成二進位，並統計 1 的數量。"""
    bits = []
    ones = 0

    while n > 0:
        bit = n % 2
        bits.append(str(bit))
        if bit == 1:
            ones += 1
        n //= 2

    bits.reverse()
    return "".join(bits), ones


def parity_line_easy(n: int) -> str:
    """回傳題目要求的輸出字串。"""
    b, p = to_binary_and_ones_easy(n)
    return f"The parity of {b} is {p} (mod 2)."


def solve_all_easy(text: str) -> str:
    """逐行輸入，0 表示結束。"""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue

        v = int(s)
        if v == 0:
            break

        out.append(parity_line_easy(v))

    return "\n".join(out)


def main() -> None:
    import sys

    src = sys.stdin.read()
    res = solve_all_easy(src)
    if res:
        print(res)


if __name__ == "__main__":
    main()
