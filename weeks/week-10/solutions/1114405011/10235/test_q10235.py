from __future__ import annotations

import os
import subprocess
import sys
import unittest
from typing import List, Tuple


def run_script(filename: str, input_data: str) -> str:
    """執行同資料夾下的解題程式，回傳標準輸出。"""
    here = os.path.dirname(__file__)
    path = os.path.join(here, filename)
    proc = subprocess.run(
        [sys.executable, path],
        input=input_data,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout


def brute_force_cycle_cover_count(grid: List[List[int]]) -> int:
    """小尺寸暴力驗證：統計所有讓每個 1 格度數=2、每個 0 格度數=0 的邊配置數。"""
    n = len(grid)
    m = len(grid[0]) if n else 0

    edges: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    for r in range(n):
        for c in range(m):
            if grid[r][c] != 1:
                continue
            if c + 1 < m and grid[r][c + 1] == 1:
                edges.append(((r, c), (r, c + 1)))
            if r + 1 < n and grid[r + 1][c] == 1:
                edges.append(((r, c), (r + 1, c)))

    ans = 0
    for mask in range(1 << len(edges)):
        deg = [[0] * m for _ in range(n)]
        ok = True

        for i, (a, b) in enumerate(edges):
            if (mask >> i) & 1:
                ar, ac = a
                br, bc = b
                deg[ar][ac] += 1
                deg[br][bc] += 1
                if deg[ar][ac] > 2 or deg[br][bc] > 2:
                    ok = False
                    break

        if not ok:
            continue

        for r in range(n):
            for c in range(m):
                if grid[r][c] == 1 and deg[r][c] != 2:
                    ok = False
                    break
                if grid[r][c] == 0 and deg[r][c] != 0:
                    ok = False
                    break
            if not ok:
                break

        if ok:
            ans += 1

    return ans


class TestQ10235(unittest.TestCase):
    def test_small_grids(self) -> None:
        grids = [
            [[1]],
            [[1, 1], [1, 1]],
            [[1, 0], [1, 1]],
        ]

        lines = [str(len(grids))]
        expected_lines = []

        for i, g in enumerate(grids, start=1):
            n = len(g)
            m = len(g[0])
            lines.append(f"{n} {m}")
            for row in g:
                lines.append("".join(str(x) for x in row))

            expected_lines.append(f"Case {i}: {brute_force_cycle_cover_count(g)}")

        inp = "\n".join(lines) + "\n"
        expected = "\n".join(expected_lines)

        self.assertEqual(run_script("q10235.py", inp), expected)
        self.assertEqual(run_script("q10235-easy.py", inp), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
