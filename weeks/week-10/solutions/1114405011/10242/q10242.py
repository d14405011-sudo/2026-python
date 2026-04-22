"""
題號 10242 一般版解法（ATM）

核心觀念：
1) 原圖可重複走邊與節點，但每個點的 ATM 只可搶一次。
2) 在強連通分量（SCC）內可互相到達，因此同一 SCC 的 ATM 金額可一次性加總。
3) 把 SCC 縮點後得到 DAG，問題轉為：
   從起點 SCC 出發，在 DAG 上走到任一酒吧 SCC 的最大路徑和。
"""

from __future__ import annotations

from collections import deque
from typing import Deque, List, Set


def scc_kosaraju(n: int, g: List[List[int]], rg: List[List[int]]) -> tuple[List[int], int]:
    """Kosaraju：回傳每個點所屬 SCC 編號與 SCC 數量。"""
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
    cid = 0

    def dfs2(u: int, c: int) -> None:
        comp[u] = c
        for v in rg[u]:
            if comp[v] == -1:
                dfs2(v, c)

    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u, cid)
            cid += 1

    return comp, cid


def max_loot(
    n: int,
    edges: List[tuple[int, int]],
    money: List[int],
    start: int,
    bars: Set[int],
) -> int:
    g = [[] for _ in range(n + 1)]
    rg = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        rg[v].append(u)

    comp, cnum = scc_kosaraju(n, g, rg)

    scc_sum = [0] * cnum
    scc_bar = [False] * cnum
    for u in range(1, n + 1):
        cu = comp[u]
        scc_sum[cu] += money[u]
        if u in bars:
            scc_bar[cu] = True

    dag = [set() for _ in range(cnum)]
    indeg = [0] * cnum
    for u, v in edges:
        cu, cv = comp[u], comp[v]
        if cu != cv and cv not in dag[cu]:
            dag[cu].add(cv)
            indeg[cv] += 1

    start_c = comp[start]

    # 先從起點 SCC 做可達性，避免處理與答案無關的節點
    reachable = [False] * cnum
    q: Deque[int] = deque([start_c])
    reachable[start_c] = True
    while q:
        u = q.popleft()
        for v in dag[u]:
            if not reachable[v]:
                reachable[v] = True
                q.append(v)

    # 在 DAG 上做拓樸序，再進行最長路 DP
    indeg2 = indeg[:]
    topo: List[int] = []
    q2: Deque[int] = deque(i for i in range(cnum) if indeg2[i] == 0)
    while q2:
        u = q2.popleft()
        topo.append(u)
        for v in dag[u]:
            indeg2[v] -= 1
            if indeg2[v] == 0:
                q2.append(v)

    NEG = -10**30
    dist = [NEG] * cnum
    dist[start_c] = scc_sum[start_c]

    for u in topo:
        if dist[u] == NEG or not reachable[u]:
            continue
        for v in dag[u]:
            if reachable[v] and dist[v] < dist[u] + scc_sum[v]:
                dist[v] = dist[u] + scc_sum[v]

    ans = 0
    for c in range(cnum):
        if reachable[c] and scc_bar[c] and dist[c] > ans:
            ans = dist[c]
    return ans


def solve(raw: str) -> str:
    it = iter(raw.strip().split())

    n = int(next(it))
    m = int(next(it))

    edges: List[tuple[int, int]] = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        edges.append((u, v))

    money = [0] * (n + 1)
    for i in range(1, n + 1):
        money[i] = int(next(it))

    start = int(next(it))
    p = int(next(it))
    bars = {int(next(it)) for _ in range(p)}

    return str(max_loot(n, edges, money, start, bars))


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print(solve(data), end="")
