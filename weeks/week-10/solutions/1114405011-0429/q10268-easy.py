"""
題號 10268 -easy 版

直覺記憶法：
- 測試次數 m 每加 1，我們可判定的樓層會大幅增加。
- 設 reachable[e] = 目前 m 次、e 顆球可保證判定的最大樓層。
- 轉移：reachable[e] = reachable[e] + reachable[e-1] + 1

最多只需檢查到 63 次；超過就印固定字串。
"""

from __future__ import annotations

from typing import List, Optional


LIMIT_MSG = "More than 63 trials needed."


def least_moves(eggs: int, floors: int) -> Optional[int]:
    if floors <= 0:
        return 0

    reachable = [0] * (eggs + 1)

    for moves in range(1, 64):
        for e in range(eggs, 0, -1):
            reachable[e] = reachable[e] + reachable[e - 1] + 1
            if reachable[e] > floors:
                reachable[e] = floors
        if reachable[eggs] >= floors:
            return moves

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

        ans = least_moves(k, n)
        if ans is None:
            out.append(LIMIT_MSG)
        else:
            out.append(str(ans))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
