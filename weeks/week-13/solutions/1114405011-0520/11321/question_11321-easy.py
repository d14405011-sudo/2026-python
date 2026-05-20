"""UVA 11321（本課版本：放陷阱但不能封路）
簡單好記版：含繁體中文詳細註解
"""

from __future__ import annotations

from collections import deque


def ok(n: int, m: int, bad: list[list[bool]]) -> bool:
    """只要左邊走得到右邊，就代表這次放陷阱是合法的。"""
    q: deque[tuple[int, int]] = deque()
    vis = [[False] * m for _ in range(n)]

    for x in range(n):
        if not bad[x][0]:
            vis[x][0] = True
            q.append((x, 0))

    while q:
        x, y = q.popleft()
        if y == m - 1:
            return True

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not bad[nx][ny] and not vis[nx][ny]:
                vis[nx][ny] = True
                q.append((nx, ny))

    return False


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    if not a:
        return ""

    n, m, t = a[0], a[1], a[2]
    p = 3

    bad = [[False] * m for _ in range(n)]
    ans: list[str] = []

    for _ in range(t):
        x, y = a[p], a[p + 1]
        p += 2

        bad[x][y] = True
        if ok(n, m, bad):
            ans.append("<(_ _)>")
        else:
            bad[x][y] = False
            ans.append(">_<")

    return "\n".join(ans)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
