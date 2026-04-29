"""
題號 10226 -opt 版（優化）

相較 easy 版的改進：
1. parse_input 改用逐 token 迭代器讀取，移除複雜的 T 格式自動偵測
   try/except 邏輯，程式碼更短且更可靠。
2. 人名列表改用 string.ascii_uppercase 切片，更 Pythonic。
3. list_valid_orders 中合併 used[i] 與 position in banned[i] 為單一條件，
   減少縮排層次。
4. keep_only_changed_suffix 改用 os.path.commonprefix 計算公共前綴，
   以內建 C 實作取代手寫 Python while 迴圈。
"""

from __future__ import annotations

import os
import string
from typing import List, Set, Tuple


def parse_input(raw: str) -> List[Tuple[int, List[Set[int]]]]:
    it = iter(raw.split())
    t = int(next(it))
    cases: List[Tuple[int, List[Set[int]]]] = []

    for _ in range(t):
        n = int(next(it))
        banned: List[Set[int]] = []
        for _ in range(n):
            s: Set[int] = set()
            while True:
                v = int(next(it))
                if v == 0:
                    break
                s.add(v)
            banned.append(s)
        cases.append((n, banned))

    return cases


def list_valid_orders(n: int, banned: List[Set[int]]) -> List[str]:
    people = list(string.ascii_uppercase[:n])
    used = [False] * n
    order: List[str] = [""] * n
    all_orders: List[str] = []

    def dfs(pos: int) -> None:
        if pos == n:
            all_orders.append("".join(order))
            return
        position = pos + 1
        for i in range(n):
            if used[i] or position in banned[i]:
                continue
            used[i] = True
            order[pos] = people[i]
            dfs(pos + 1)
            used[i] = False

    dfs(0)
    return all_orders


def keep_only_changed_suffix(lines: List[str]) -> List[str]:
    if not lines:
        return []
    out = [lines[0]]
    for prev, curr in zip(lines, lines[1:]):
        p = len(os.path.commonprefix([prev, curr]))
        out.append(curr[p:])
    return out


def solve(raw: str) -> str:
    cases = parse_input(raw)
    result: List[str] = []

    for i, (n, banned) in enumerate(cases):
        orders = list_valid_orders(n, banned)
        result.extend(keep_only_changed_suffix(orders))
        if i != len(cases) - 1:
            result.append("")

    return "\n".join(result)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
