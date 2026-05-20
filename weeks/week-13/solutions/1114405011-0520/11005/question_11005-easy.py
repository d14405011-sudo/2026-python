"""UVA 11005 - Cheapest Base
簡單好記版：含繁體中文詳細註解
"""

from __future__ import annotations


def one_cost(n: int, b: int, costs: list[int]) -> int:
    """把十進位 n 轉成 b 進位後，累加每一位的成本。"""
    if n == 0:
        return costs[0]

    s = 0
    while n:
        s += costs[n % b]
        n //= b
    return s


def best_bases(n: int, costs: list[int]) -> list[int]:
    """從 2~36 進位裡，挑出最便宜的所有進位。"""
    c = [one_cost(n, b, costs) for b in range(2, 37)]
    m = min(c)
    return [idx + 2 for idx, v in enumerate(c) if v == m]


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    p = 0
    t = a[p]
    p += 1

    ans: list[str] = []
    for case_id in range(1, t + 1):
        costs = a[p : p + 36]
        p += 36

        q = a[p]
        p += 1

        ans.append(f"Case {case_id}:")

        for _ in range(q):
            n = a[p]
            p += 1
            ans.append(
                f"Cheapest base(s) for number {n}: "
                + " ".join(map(str, best_bases(n, costs)))
            )

        if case_id != t:
            ans.append("")

    return "\n".join(ans)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
