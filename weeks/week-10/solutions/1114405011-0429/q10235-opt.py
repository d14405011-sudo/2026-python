"""
題號 10235 -opt 版（優化）

相較 easy 版的改進：
1. states 與 nxt 字典改用 defaultdict(int)，省去所有手動 .get(key, 0)
   呼叫，程式碼更簡潔。
2. can_right / can_down 旗標在進入格子前先計算並快取，避免在內層迴圈
   重複存取 grid 陣列。
3. 移除 right_candidates / down_candidates 中間列表，改用 (0, 1) tuple
   配合 continue 跳過無效值，減少不必要的列表建立。
4. 下邊 bitmask 設定簡化為 next_mask | (down << c)，省去 if down == 1
   的判斷分支。
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

MOD = 1_000_000_007


def count_snake_layouts(grid: List[List[int]]) -> int:
    n = len(grid)
    m = len(grid[0]) if n else 0

    row_dp: Dict[int, int] = {0: 1}

    for r in range(n):
        new_row_dp: Dict[int, int] = defaultdict(int)

        for up_mask, base_ways in row_dp.items():
            states: Dict[tuple, int] = defaultdict(int)
            states[(0, 0)] = base_ways

            for c in range(m):
                nxt: Dict[tuple, int] = defaultdict(int)
                can_right = c + 1 < m and grid[r][c + 1] == 1
                can_down  = r + 1 < n and grid[r + 1][c] == 1

                for (next_mask, left), ways in states.items():
                    up = (up_mask >> c) & 1
                    is_open = grid[r][c] == 1

                    if not is_open:
                        if up == 0 and left == 0:
                            nxt[(next_mask, 0)] = (nxt[(next_mask, 0)] + ways) % MOD
                        continue

                    for right in (0, 1):
                        if right and not can_right:
                            continue
                        for down in (0, 1):
                            if down and not can_down:
                                continue
                            if up + left + right + down != 2:
                                continue
                            nm = next_mask | (down << c)
                            nxt[(nm, right)] = (nxt[(nm, right)] + ways) % MOD

                states = nxt

            for (next_mask, left), ways in states.items():
                if left == 0:
                    new_row_dp[next_mask] = (new_row_dp[next_mask] + ways) % MOD

        row_dp = new_row_dp

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
