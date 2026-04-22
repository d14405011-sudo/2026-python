from __future__ import annotations

from typing import Dict, List

MOD = 1_000_000_007


def count_layouts(grid: List[List[int]]) -> int:
    n = len(grid)
    m = len(grid[0]) if n else 0
    row_dp: Dict[int, int] = {0: 1}

    for r in range(n):
        new_row: Dict[int, int] = {}
        for up_mask, base in row_dp.items():
            states: Dict[tuple[int, int], int] = {(0, 0): base}
            for c in range(m):
                nxt: Dict[tuple[int, int], int] = {}
                for (next_mask, left), ways in states.items():
                    up = (up_mask >> c) & 1
                    if grid[r][c] == 0:
                        if up == 0 and left == 0:
                            k = (next_mask, 0)
                            nxt[k] = (nxt.get(k, 0) + ways) % MOD
                        continue

                    rights = [0]
                    if c + 1 < m and grid[r][c + 1] == 1:
                        rights.append(1)
                    downs = [0]
                    if r + 1 < n and grid[r + 1][c] == 1:
                        downs.append(1)

                    for right in rights:
                        for down in downs:
                            if up + left + right + down != 2:
                                continue
                            nm = next_mask
                            if down:
                                nm |= 1 << c
                            k = (nm, right)
                            nxt[k] = (nxt.get(k, 0) + ways) % MOD
                states = nxt

            for (next_mask, left), ways in states.items():
                if left == 0:
                    new_row[next_mask] = (new_row.get(next_mask, 0) + ways) % MOD
        row_dp = new_row

    return row_dp.get(0, 0)


def solve(raw: str) -> str:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    t = int(lines[0])
    i = 1
    out = []

    for cid in range(1, t + 1):
        n, m = map(int, lines[i].split())
        i += 1
        grid = []
        for _ in range(n):
            s = lines[i].replace(" ", "")
            i += 1
            grid.append([1 if ch == "1" else 0 for ch in s])
        out.append(f"Case {cid}: {count_layouts(grid)}")

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
