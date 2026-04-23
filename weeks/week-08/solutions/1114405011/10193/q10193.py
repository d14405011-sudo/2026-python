"""
UVA 10193 - All You Need Is Love

做法：
- 每組輸入有兩個二進位字串。
- 轉成整數後取最大公因數 gcd。
- gcd > 1 代表可被同一質因數整除，輸出 love 句子。
"""

from math import gcd


def solve_case(a_bin: str, b_bin: str, idx: int) -> str:
    """解單一測資並產生題目格式輸出。"""
    a = int(a_bin, 2)
    b = int(b_bin, 2)
    if gcd(a, b) > 1:
        return f"Pair #{idx}: All you need is love!"
    return f"Pair #{idx}: Love is not all you need!"


def solve_all(text: str) -> str:
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    out: list[str] = []
    pos = 1

    for i in range(1, t + 1):
        a_bin = lines[pos]
        b_bin = lines[pos + 1]
        pos += 2
        out.append(solve_case(a_bin, b_bin, i))

    return "\n".join(out)


def main() -> None:
    import sys

    data = sys.stdin.read()
    ans = solve_all(data)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
