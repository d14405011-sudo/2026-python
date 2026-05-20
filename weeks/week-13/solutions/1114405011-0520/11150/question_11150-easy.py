"""UVA 11150（本課版本：青蛙過河最少踩石）
簡單好記版：含繁體中文詳細註解
"""

from __future__ import annotations


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    if not a:
        return ""

    l = a[0]
    s, t, m = a[1], a[2], a[3]
    stones = sorted(x for x in a[4 : 4 + m] if 0 < x < l)

    # 跳距固定時，青蛙每次都落在固定座標上。
    if s == t:
        ans = sum(1 for x in stones if x % s == 0)
        return str(ans)

    # 把很長空白區段壓成固定長度，保留可達性但降低 DP 長度。
    MAX_GAP = 100
    comp = 0
    prev = 0
    pos = []
    for x in stones:
        comp += min(x - prev, MAX_GAP)
        pos.append(comp)
        prev = x

    end = comp + min(l - prev, MAX_GAP)

    stone = [0] * (end + t + 1)
    for p in pos:
        stone[p] = 1

    INF = 10**9
    dp = [INF] * (end + t + 1)
    dp[0] = 0

    for i in range(1, end + t + 1):
        best = INF
        for step in range(s, t + 1):
            if i - step >= 0:
                best = min(best, dp[i - step])
        if best < INF:
            dp[i] = best + stone[i]

    return str(min(dp[end : end + t + 1]))


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
