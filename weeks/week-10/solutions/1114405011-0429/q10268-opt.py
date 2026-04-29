"""
題號 10268 -opt 版（優化）

相較 easy 版的改進：
1. 移除內迴圈中不必要的 floors 上限截斷（原本的
     if reachable[e] > floors: reachable[e] = floors）。
   Python 整數無溢位問題，截斷只會讓值停留在較小數字，
   反而需要更多輪次才能觸發外層的提前結束條件。
   移除截斷後 reachable 值自然增長，外層迴圈更早結束。
2. 輸入解析改用 line.split() 取 parts[0]/parts[1]，
   省去 line.strip() 的額外呼叫，並用 len(parts) < 2 防止空行。
"""

from __future__ import annotations

from typing import List, Optional


LIMIT_MSG = "More than 63 trials needed."


def least_moves(eggs: int, floors: int) -> Optional[int]:
    if floors <= 0:
        return 0

    reachable = [0] * (eggs + 1)

    for moves in range(1, 64):
        # 由大到小更新，確保使用上一輪的舊值（原地滾動 DP）
        for e in range(eggs, 0, -1):
            reachable[e] += reachable[e - 1] + 1
        if reachable[eggs] >= floors:
            return moves

    return None


def solve(raw: str) -> str:
    out: List[str] = []

    for line in raw.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        k, n = int(parts[0]), int(parts[1])
        if k == 0:
            break

        ans = least_moves(k, n)
        out.append(LIMIT_MSG if ans is None else str(ans))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
