"""
題號 10235 一般版解法

題意可視為：
- 0 代表插座，不可被蛇佔據。
- 1 代表可佔據格，且每個可佔據格都必須被蛇身覆蓋。
- 蛇都咬尾巴，所以每隻蛇是環。

在格點圖中等價為：
對每個可佔據格，從其四鄰邊中挑選邊，使該點度數恰為 2；
對插座格，度數必為 0。
如此每個連通分量自然形成一個或多個環（可多條蛇）。

做法：逐格掃描的狀態 DP（profile DP）
- up_mask：上一列往下接到本列的垂直邊狀態。
- left：目前格子的左邊是否有邊接入。
- 對當前格決定 right/down 是否開邊，滿足度數條件即可轉移。
"""

from __future__ import annotations

from typing import Dict, List

MOD = 1_000_000_007


def count_ways(grid: List[List[int]]) -> int:
    n = len(grid)
    m = len(grid[0]) if n else 0

    # dp_masks[mask] = 處理到第 i 列前，來自上一列的「往下邊」型態為 mask 的方法數
    dp_masks: Dict[int, int] = {0: 1}

    for i in range(n):
        next_row_dp: Dict[int, int] = {}

        for up_mask, ways0 in dp_masks.items():
            # 在同一列內逐格掃描，狀態含：
            # next_mask：本列往下一列的垂直邊配置（逐欄建立）
            # left：當前格左側是否有水平邊接入
            states: Dict[tuple[int, int], int] = {(0, 0): ways0}

            for j in range(m):
                new_states: Dict[tuple[int, int], int] = {}
                for (next_mask, left), ways in states.items():
                    up = (up_mask >> j) & 1
                    open_cell = grid[i][j] == 1

                    if not open_cell:
                        # 插座格不能有任何邊接入
                        if up == 0 and left == 0:
                            key = (next_mask, 0)
                            new_states[key] = (new_states.get(key, 0) + ways) % MOD
                        continue

                    # 可佔據格必須度數=2，列舉 right/down 是否開邊
                    right_options = [0]
                    if j + 1 < m and grid[i][j + 1] == 1:
                        right_options.append(1)

                    down_options = [0]
                    if i + 1 < n and grid[i + 1][j] == 1:
                        down_options.append(1)

                    for right in right_options:
                        for down in down_options:
                            deg = up + left + right + down
                            if deg != 2:
                                continue
                            nm = next_mask
                            if down:
                                nm |= 1 << j
                            key = (nm, right)
                            new_states[key] = (new_states.get(key, 0) + ways) % MOD

                states = new_states

            # 一列結束時，最後一格右邊不應殘留邊（left 必須回到 0）
            for (next_mask, left), ways in states.items():
                if left != 0:
                    continue
                next_row_dp[next_mask] = (next_row_dp.get(next_mask, 0) + ways) % MOD

        dp_masks = next_row_dp

    # 所有列結束後，不可再有往下懸空邊
    return dp_masks.get(0, 0)


def solve(raw: str) -> str:
    it = iter(raw.strip().splitlines())
    t = int(next(it))
    out: List[str] = []

    for case_idx in range(1, t + 1):
        n, m = map(int, next(it).split())
        grid: List[List[int]] = []
        for _ in range(n):
            line = next(it).strip().replace(" ", "")
            grid.append([1 if ch == "1" else 0 for ch in line])

        ans = count_ways(grid)
        out.append(f"Case {case_idx}: {ans}")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print(solve(data), end="")
