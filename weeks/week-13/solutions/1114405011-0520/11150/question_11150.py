"""UVA 11150（本課版本：青蛙過河最少踩石）
一般版：含繁體中文註解
"""

from __future__ import annotations

INF = 10**9


def solve_case(l: int, s: int, t: int, stones: list[int]) -> int:
    stones = sorted(x for x in stones if 0 < x < l)

    # 若每次跳躍距離固定，路徑唯一，直接數可達位置上的石頭即可。
    if s == t:
        step = s
        return sum(1 for x in stones if x % step == 0)

    # 座標壓縮：大間距只保留到常數上限，避免 L 很大時陣列爆炸。
    MAX_GAP = 100
    comp_pos: list[int] = []
    prev = 0
    comp = 0

    for x in stones:
        gap = x - prev
        comp += min(gap, MAX_GAP)
        comp_pos.append(comp)
        prev = x

    comp_l = comp + min(l - prev, MAX_GAP)

    has_stone = [0] * (comp_l + t + 1)
    for p in comp_pos:
        has_stone[p] = 1

    dp = [INF] * (comp_l + t + 1)
    dp[0] = 0

    for i in range(1, comp_l + t + 1):
        best = INF
        for jump in range(s, t + 1):
            if i - jump >= 0:
                best = min(best, dp[i - jump])
        if best < INF:
            dp[i] = best + has_stone[i]

    return min(dp[comp_l : comp_l + t + 1])


def solve(text: str) -> str:
    vals = list(map(int, text.split()))
    if not vals:
        return ""

    i = 0
    l = vals[i]
    i += 1
    s = vals[i]
    t = vals[i + 1]
    m = vals[i + 2]
    i += 3
    stones = vals[i : i + m]

    return str(solve_case(l, s, t, stones))


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
