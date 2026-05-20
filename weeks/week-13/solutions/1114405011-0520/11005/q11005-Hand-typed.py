from __future__ import annotations


def f(n: int, b: int, c: list[int]) -> int:
    if n == 0:
        return c[0]
    s = 0
    while n:
        s += c[n % b]
        n //= b
    return s


def g(n: int, c: list[int]) -> list[int]:
    arr = [(b, f(n, b, c)) for b in range(2, 37)]
    m = min(v for _, v in arr)
    return [b for b, v in arr if v == m]


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    i = 0
    t = a[i]
    i += 1
    out: list[str] = []

    for k in range(1, t + 1):
        c = a[i : i + 36]
        i += 36
        q = a[i]
        i += 1
        out.append(f"Case {k}:")

        for _ in range(q):
            n = a[i]
            i += 1
            out.append(f"Cheapest base(s) for number {n}: " + " ".join(map(str, g(n, c))))

        if k != t:
            out.append("")

    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
