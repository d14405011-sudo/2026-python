from __future__ import annotations


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    if not a:
        return ""

    l = a[0]
    s, t, m = a[1], a[2], a[3]
    st = sorted(x for x in a[4 : 4 + m] if 0 < x < l)

    if s == t:
        return str(sum(1 for x in st if x % s == 0))

    MAX_GAP = 100
    c = 0
    p = 0
    arr = []
    for x in st:
        c += min(x - p, MAX_GAP)
        arr.append(c)
        p = x
    end = c + min(l - p, MAX_GAP)

    mark = [0] * (end + t + 1)
    for x in arr:
        mark[x] = 1

    INF = 10**9
    dp = [INF] * (end + t + 1)
    dp[0] = 0

    for i in range(1, end + t + 1):
        v = INF
        for d in range(s, t + 1):
            if i - d >= 0 and dp[i - d] < v:
                v = dp[i - d]
        if v < INF:
            dp[i] = v + mark[i]

    return str(min(dp[end : end + t + 1]))


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
