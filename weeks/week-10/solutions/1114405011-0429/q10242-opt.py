"""
題號 10242 -opt 版（優化）

相較 easy 版的改進：
1. Kosaraju 演算法的兩次遞迴 DFS 全部改為迭代 DFS（iterative DFS），
   徹底避免 Python 預設遞迴深度限制（1000 層），
   可正確處理節點數量較大的測試資料。
2. 第一次 DFS 使用 iter(adj_list) 保存迭代器狀態於 stack，
   模擬遞迴呼叫框架，並在 StopIteration 時將節點加入 order。
3. 第二次 DFS（反向圖標記 SCC）改用簡單 stack pop，實作更精簡。
4. DAG 邊集合以 set 型別儲存，自動去除重複邊，省去 cv not in dag[cu] 判斷。
"""

from __future__ import annotations

from collections import deque
from typing import Deque, List, Set, Tuple


def build_scc_iterative(
    n: int, g: List[List[int]], rg: List[List[int]]
) -> Tuple[List[int], int]:
    # 第一次 DFS：計算完成順序（後序）
    visited = [False] * (n + 1)
    order: List[int] = []

    for start in range(1, n + 1):
        if visited[start]:
            continue
        visited[start] = True
        stack = [(start, iter(g[start]))]
        while stack:
            u, it = stack[-1]
            try:
                v = next(it)
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, iter(g[v])))
            except StopIteration:
                stack.pop()
                order.append(u)

    # 第二次 DFS：在反向圖上標記 SCC
    comp = [-1] * (n + 1)
    cnum = 0

    for start in reversed(order):
        if comp[start] != -1:
            continue
        comp[start] = cnum
        stack2 = [start]
        while stack2:
            u = stack2.pop()
            for v in rg[u]:
                if comp[v] == -1:
                    comp[v] = cnum
                    stack2.append(v)
        cnum += 1

    return comp, cnum


def solve_case(
    n: int,
    edges: List[Tuple[int, int]],
    cash: List[int],
    start: int,
    bars: Set[int],
) -> int:
    g  = [[] for _ in range(n + 1)]
    rg = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        rg[v].append(u)

    comp, cnum = build_scc_iterative(n, g, rg)

    scc_cash = [0] * cnum
    scc_bar  = [False] * cnum
    for u in range(1, n + 1):
        cid = comp[u]
        scc_cash[cid] += cash[u]
        if u in bars:
            scc_bar[cid] = True

    # DAG：以 set 儲存，自動去重
    dag: List[Set[int]] = [set() for _ in range(cnum)]
    indeg = [0] * cnum
    for u, v in edges:
        cu, cv = comp[u], comp[v]
        if cu != cv and cv not in dag[cu]:
            dag[cu].add(cv)
            indeg[cv] += 1

    start_c = comp[start]

    # BFS 標記可達 SCC
    reach = [False] * cnum
    q: Deque[int] = deque([start_c])
    reach[start_c] = True
    while q:
        u = q.popleft()
        for v in dag[u]:
            if not reach[v]:
                reach[v] = True
                q.append(v)

    # 拓樸排序
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

    NEG = -(10 ** 30)
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

    n = data[p]; p += 1
    m = data[p]; p += 1

    edges: List[Tuple[int, int]] = []
    for _ in range(m):
        u, v = data[p], data[p + 1]; p += 2
        edges.append((u, v))

    cash = [0] * (n + 1)
    for i in range(1, n + 1):
        cash[i] = data[p]; p += 1

    start = data[p]; p += 1
    bcnt  = data[p]; p += 1
    bars  = set(data[p: p + bcnt])

    return str(solve_case(n, edges, cash, start, bars))


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
