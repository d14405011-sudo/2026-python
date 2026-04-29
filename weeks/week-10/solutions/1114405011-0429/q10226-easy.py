"""
題號 10226 -easy 版

這一版刻意用「一步一步直覺思考」來寫，方便背誦：
1) 先把每個人的禁站位置讀好。
2) 依照位置 1..N 來放人。
3) 每一步都從 A 開始嘗試，天然就是字典序。
4) 產生完整排列後，再做「只輸出和前一筆不同的後綴」。
"""

from __future__ import annotations

from typing import List, Set, Tuple


def parse_input(raw: str) -> List[Tuple[int, List[Set[int]]]]:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        return []

    # 這裡採「讀到 EOF」的簡單格式。
    # 若第一行其實是 T，使用者也可自行把每組拆開餵入。
    idx = 0
    cases: List[Tuple[int, List[Set[int]]]] = []

    # 嘗試 T 格式：第一行若可完整切出 T 組就採用
    try:
        t = int(lines[0])
        idx2 = 1
        tmp: List[Tuple[int, List[Set[int]]]] = []
        ok = True
        for _ in range(t):
            if idx2 >= len(lines):
                ok = False
                break
            n = int(lines[idx2])
            idx2 += 1
            if idx2 + n > len(lines):
                ok = False
                break
            banned: List[Set[int]] = []
            for _ in range(n):
                nums = list(map(int, lines[idx2].split()))
                idx2 += 1
                s: Set[int] = set()
                for v in nums:
                    if v == 0:
                        break
                    s.add(v)
                banned.append(s)
            tmp.append((n, banned))
        if ok and idx2 == len(lines):
            return tmp
    except Exception:
        pass

    while idx < len(lines):
        n = int(lines[idx])
        idx += 1
        banned: List[Set[int]] = []
        for _ in range(n):
            nums = list(map(int, lines[idx].split()))
            idx += 1
            s: Set[int] = set()
            for v in nums:
                if v == 0:
                    break
                s.add(v)
            banned.append(s)
        cases.append((n, banned))

    return cases


def list_valid_orders(n: int, banned: List[Set[int]]) -> List[str]:
    people = [chr(ord("A") + i) for i in range(n)]
    used = [False] * n
    order = [""] * n
    all_orders: List[str] = []

    def dfs(pos: int) -> None:
        if pos == n:
            all_orders.append("".join(order))
            return

        position = pos + 1
        for i in range(n):
            if used[i]:
                continue
            if position in banned[i]:
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
    for i in range(1, len(lines)):
        a = lines[i - 1]
        b = lines[i]
        p = 0
        while p < len(a) and p < len(b) and a[p] == b[p]:
            p += 1
        out.append(b[p:])
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
