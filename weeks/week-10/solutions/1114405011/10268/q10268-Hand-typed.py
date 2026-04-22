from __future__ import annotations

from typing import Optional


def least_moves(k: int, n: int) -> Optional[int]:
    if n <= 0:
        return 0
    dp = [0] * (k + 1)
    for m in range(1, 64):
        for e in range(k, 0, -1):
            dp[e] = dp[e] + dp[e - 1] + 1
            if dp[e] > n:
                dp[e] = n
        if dp[k] >= n:
            return m
    return None


def solve(raw: str) -> str:
    out = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        k, n = map(int, line.split())
        if k == 0:
            break
        ans = least_moves(k, n)
        out.append(str(ans) if ans is not None else "More than 63 trials needed.")
    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
