"""
UVA 10190 - Divide, But Not Quite Conquer!

規則：
- 給定 n, m。
- 若可形成序列 n, n/m, n/m^2, ..., 1 且每一步都整除，輸出整個序列。
- 否則輸出 Boring!
"""


def build_sequence(n: int, m: int) -> list[int] | None:
    """回傳合法序列；若不合法回傳 None。"""
    if n < 1 or m < 2:
        return None

    seq = [n]
    while n != 1:
        if n % m != 0:
            return None
        n //= m
        seq.append(n)

    return seq


def solve_line(n: int, m: int) -> str:
    seq = build_sequence(n, m)
    if seq is None:
        return "Boring!"
    return " ".join(map(str, seq))


def solve_all(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        n, m = map(int, line.split())
        out.append(solve_line(n, m))
    return "\n".join(out)


def main() -> None:
    import sys

    data = sys.stdin.read()
    ans = solve_all(data)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
