"""
題號 10268 一般版解法（丟水球 / 雞蛋掉落）

目標：
給定 k 顆球、n 層樓，求最壞情況下最少測試次數。
若超過 63 次，輸出指定訊息。

經典 DP：
令 dp[e] 為「目前測了 m 次、用 e 顆球最多可判定幾層樓」。
轉移：dp[e] = dp[e] + dp[e-1] + 1
含義：
- 本次球破：可處理下方 dp[e-1] 層
- 本次球不破：可處理上方 dp[e] 層
- 再加當前測試樓層 1

逐步增加 m（1..63），直到 dp[k] >= n。
"""

from __future__ import annotations

from typing import List, Optional


def min_trials(k: int, n: int) -> Optional[int]:
    if n <= 0:
        return 0

    dp = [0] * (k + 1)

    for m in range(1, 64):
        # 逆序更新，避免本輪覆寫到 dp[e-1] 的舊值
        for e in range(k, 0, -1):
            dp[e] = dp[e] + dp[e - 1] + 1
            if dp[e] > n:
                dp[e] = n
        if dp[k] >= n:
            return m

    return None


def solve(raw: str) -> str:
    out: List[str] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        k, n = map(int, line.split())
        if k == 0:
            break

        ans = min_trials(k, n)
        if ans is None:
            out.append("More than 63 trials needed.")
        else:
            out.append(str(ans))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print(solve(data), end="")
