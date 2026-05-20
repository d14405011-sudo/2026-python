"""UVA 11005 - Cheapest Base
一般版：含繁體中文註解
"""

from __future__ import annotations


def cost_in_base(number: int, base: int, costs: list[int]) -> int:
    """計算 number 在指定進位 base 下的印刷成本。"""
    if number == 0:
        return costs[0]

    total = 0
    n = number
    while n > 0:
        digit = n % base
        total += costs[digit]
        n //= base
    return total


def cheapest_bases(number: int, costs: list[int]) -> list[int]:
    """找出成本最低的所有進位（2..36）。"""
    all_costs = []
    for base in range(2, 37):
        all_costs.append((base, cost_in_base(number, base, costs)))

    best = min(c for _, c in all_costs)
    return [b for b, c in all_costs if c == best]


def solve(data: str) -> str:
    vals = list(map(int, data.split()))
    i = 0
    t = vals[i]
    i += 1

    out: list[str] = []
    for case_no in range(1, t + 1):
        # 題目固定每組有 36 個符號成本（0-9, A-Z）。
        costs = vals[i : i + 36]
        i += 36

        q = vals[i]
        i += 1

        out.append(f"Case {case_no}:")

        for _ in range(q):
            n = vals[i]
            i += 1
            bases = cheapest_bases(n, costs)
            out.append(
                f"Cheapest base(s) for number {n}: " + " ".join(map(str, bases))
            )

        if case_no != t:
            out.append("")

    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
