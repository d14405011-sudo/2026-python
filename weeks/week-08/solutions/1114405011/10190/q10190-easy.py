"""
UVA 10190 - easy 版

易記重點：
- 只記一件事：每一步都要「能整除」。
- 一旦不能整除，就直接 Boring!。
"""


def solve_line(n: int, m: int) -> str:
    if n < 1 or m < 2:
        return "Boring!"

    seq = [n]
    while n != 1:
        if n % m != 0:
            return "Boring!"
        n //= m
        seq.append(n)

    return " ".join(str(x) for x in seq)


def solve_all(text: str) -> str:
    rows = []
    for s in text.splitlines():
        s = s.strip()
        if not s:
            continue
        n, m = map(int, s.split())
        rows.append(solve_line(n, m))
    return "\n".join(rows)


def main() -> None:
    import sys

    data = sys.stdin.read()
    ans = solve_all(data)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
