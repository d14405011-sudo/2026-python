from __future__ import annotations

from collections import deque
from typing import Deque, List, Set, Tuple


def build_scc(n: int, g: List[List[int]], rg: List[List[int]]) -> Tuple[List[int], int]:
    vis = [False] * (n + 1)
    order: List[int] = []

    def dfs1(u: int) -> None:
        vis[u] = True
        for v in g[u]:
            if not vis[v]:
                dfs1(v)
        order.append(u)

    for u in range(1, n + 1):
        if not vis[u]:
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
        c = comp[u]
        scc_cash[c] += cash[u]
        if u in bars:
            scc_bar[c] = True

    dag = [set() for _ in range(cnum)]
    indeg = [0] * cnum
    for u, v in edges:
        cu, cv = comp[u], comp[v]
        if cu != cv and cv not in dag[cu]:
            dag[cu].add(cv)
            indeg[cv] += 1

    s = comp[start]
    reach = [False] * cnum
    q: Deque[int] = deque([s])
    reach[s] = True
    while q:
        u = q.popleft()
        for v in dag[u]:
            if not reach[v]:
                reach[v] = True
                q.append(v)

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
    best[s] = scc_cash[s]

    for u in topo:
        if not reach[u] or best[u] == NEG:
            continue
        for v in dag[u]:
            if reach[v]:
                cand = best[u] + scc_cash[v]
                if cand > best[v]:
                    best[v] = cand

    ans = 0
    for c in range(cnum):
        if reach[c] and scc_bar[c] and best[c] > ans:
            ans = best[c]
    return ans


def solve(raw: str) -> str:
    arr = list(map(int, raw.strip().split()))
    p = 0

    n = arr[p]
    p += 1
    m = arr[p]
    p += 1

    edges = []
    for _ in range(m):
        u, v = arr[p], arr[p + 1]
        p += 2
        edges.append((u, v))

    cash = [0] * (n + 1)
    for i in range(1, n + 1):
        cash[i] = arr[p]
        p += 1

    start = arr[p]
    p += 1
    bcnt = arr[p]
    p += 1
    bars = set(arr[p : p + bcnt])

    return str(solve_case(n, edges, cash, start, bars))


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
