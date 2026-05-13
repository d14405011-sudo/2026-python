"""UVA 10929 - Multiple of 11（好記版）

使用 11 的規則：
- 奇位數字和 - 偶位數字和
- 若差可被 11 整除，原數可被 11 整除
"""

from __future__ import annotations


def is_multiple_of_11_easy(s: str) -> bool:
    """以奇偶位和差判斷是否為 11 的倍數。"""
    odd_sum = 0
    even_sum = 0

    # 位置從 1 開始計算，符合題目常見定義。
    for idx, ch in enumerate(s, start=1):
        d = int(ch)
        if idx % 2 == 1:
            odd_sum += d
        else:
            even_sum += d

    return (odd_sum - even_sum) % 11 == 0


def solve_all_easy(text: str) -> str:
    """依題目 I/O 要求處理多行輸入。"""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s == "0":
            break

        if is_multiple_of_11_easy(s):
            out.append(f"{s} is a multiple of 11.")
        else:
            out.append(f"{s} is not a multiple of 11.")

    return "\n".join(out)


def main() -> None:
    import sys

    src = sys.stdin.read()
    res = solve_all_easy(src)
    if res:
        print(res)


if __name__ == "__main__":
    main()
