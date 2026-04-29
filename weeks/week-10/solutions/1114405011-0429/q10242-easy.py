"""
題號 10242 -easy 版

超簡化記憶法：
1) 先把「可互相來回」的一群點縮成一顆球（SCC）。
2) 每顆球的 ATM 金額先加總。
3) 球與球之間會形成一張無環圖（DAG）。
4) 從起點球做最長路，挑有酒吧的終點球最大值。
"""

from __future__ import annotations

from collections import deque
from typing import Deque, List, Set, Tuple


def build_scc(n: int, g: List[List[int]], rg: List[List[int]]) -> Tuple[List[int], int]:
    visited = [False] * (n + 1)
    order: List[int] = []

    def dfs1(u: int) -> None:
        visited[u] = True
        for v in g[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for u in range(1, n + 1):
        if not visited[u]:
            dfs1(u)

    comp = [-1] * (n + 1)
    cnum = 0

    def dfs2(u: int, cid: int) -> None:
        comp[u] = cid
        for v in rg[u]:
            if comp[v] == -1:
                dfs2(v, cid)

    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u, cnum)
            cnum += 1

    return comp, cnum


def solve_case(n: int, edges: List[Tuple[int, int]], cash: List[int], start: int, bars: Set[int]) -> int:
    g = [[] for _ in range(n + 1)]
    rg = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        rg[v].append(u)

    comp, cnum = build_scc(n, g, rg)

    scc_cash = [0] * cnum
    scc_bar = [False] * cnum
    for u in range(1, n + 1):
        cid = comp[u]
        scc_cash[cid] += cash[u]
        if u in bars:
            scc_bar[cid] = True

    dag = [set() for _ in range(cnum)]
    indeg = [0] * cnum
    for u, v in edges:
        cu, cv = comp[u], comp[v]
        if cu != cv and cv not in dag[cu]:
            dag[cu].add(cv)
            indeg[cv] += 1

    start_c = comp[start]

    # 只保留起點可達的 SCC
    reach = [False] * cnum
    q: Deque[int] = deque([start_c])
    reach[start_c] = True
    while q:
        u = q.popleft()
        for v in dag[u]:
            if not reach[v]:
                reach[v] = True
                q.append(v)

    # DAG 拓樸序
    indeg2 = indeg[:]
    topo: List[int] = []
    q2: Deque[int] = deque([i for i in range(cnum) if indeg2[i] == 0])
    while q2:
        u = q2.popleft()
        topo.append(u)
        for v in dag[u]:
            indeg2[v] -= 1
            if indeg2[v] == 0:
                q2.append(v)

    NEG = -10**30
    best = [NEG] * cnum
    best[start_c] = scc_cash[start_c]

    for u in topo:
        if best[u] == NEG or not reach[u]:
            continue
        for v in dag[u]:
            if reach[v]:
                cand = best[u] + scc_cash[v]
                if cand > best[v]:
                    best[v] = cand

    ans = 0
    for cid in range(cnum):
        if reach[cid] and scc_bar[cid] and best[cid] > ans:
            ans = best[cid]
    return ans


def solve(raw: str) -> str:
    data = list(map(int, raw.strip().split()))
    p = 0

    n = data[p]
    p += 1
    m = data[p]
    p += 1

    edges: List[Tuple[int, int]] = []
    for _ in range(m):
        u = data[p]
        v = data[p + 1]
        p += 2
        edges.append((u, v))

    cash = [0] * (n + 1)
    for i in range(1, n + 1):
        cash[i] = data[p]
        p += 1

    start = data[p]
    p += 1
    bcnt = data[p]
    p += 1
    bars = set(data[p : p + bcnt])

    return str(solve_case(n, edges, cash, start, bars))


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
