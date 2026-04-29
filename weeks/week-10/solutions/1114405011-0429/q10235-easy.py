"""
題號 10235 -easy 版

更容易記憶的口訣：
- 每個 1 格一定要「剛好接兩條邊」
- 每個 0 格一定要「一條邊都不能接」
- 用掃描線 DP：每次處理一格，只關心「上邊、左邊」已經是幾條，
  再決定「右邊、下邊」要不要開。

這樣就不需要硬記複雜圖論名詞。
"""

from __future__ import annotations

from typing import Dict, List

MOD = 1_000_000_007


def count_snake_layouts(grid: List[List[int]]) -> int:
    n = len(grid)
    m = len(grid[0]) if n else 0

    # row_dp: 上一列往下接入本列的型態 -> 方法數
    row_dp: Dict[int, int] = {0: 1}

    for r in range(n):
        new_row_dp: Dict[int, int] = {}

        for up_mask, base_ways in row_dp.items():
            # 掃描這一列時的中間狀態：
            # next_mask：本列往下的邊（準備給下一列）
            # left：當前格左邊是否有邊接進來
            states: Dict[tuple[int, int], int] = {(0, 0): base_ways}

            for c in range(m):
                nxt: Dict[tuple[int, int], int] = {}

                for (next_mask, left), ways in states.items():
                    up = (up_mask >> c) & 1
                    is_open = grid[r][c] == 1

                    if not is_open:
                        # 插座格不能有任何邊
                        if up == 0 and left == 0:
                            key = (next_mask, 0)
                            nxt[key] = (nxt.get(key, 0) + ways) % MOD
                        continue

                    right_candidates = [0]
                    if c + 1 < m and grid[r][c + 1] == 1:
                        right_candidates.append(1)

                    down_candidates = [0]
                    if r + 1 < n and grid[r + 1][c] == 1:
                        down_candidates.append(1)

                    for right in right_candidates:
                        for down in down_candidates:
                            # 對開放格，總度數必須剛好 2
                            if up + left + right + down != 2:
                                continue

                            nm = next_mask
                            if down == 1:
                                nm |= 1 << c

                            key = (nm, right)
                            nxt[key] = (nxt.get(key, 0) + ways) % MOD

                states = nxt

            # 列尾不能殘留向右的邊
            for (next_mask, left), ways in states.items():
                if left == 0:
                    new_row_dp[next_mask] = (new_row_dp.get(next_mask, 0) + ways) % MOD

        row_dp = new_row_dp

    # 最後不能再有往下懸空邊
    return row_dp.get(0, 0)


def solve(raw: str) -> str:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    t = int(lines[0])
    idx = 1
    out: List[str] = []

    for case_id in range(1, t + 1):
        n, m = map(int, lines[idx].split())
        idx += 1

        grid: List[List[int]] = []
        for _ in range(n):
            s = lines[idx].replace(" ", "")
            idx += 1
            grid.append([1 if ch == "1" else 0 for ch in s])

        ans = count_snake_layouts(grid)
        out.append(f"Case {case_id}: {ans}")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
