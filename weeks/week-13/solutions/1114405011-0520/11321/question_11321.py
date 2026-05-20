"""UVA 11321（本課版本：放陷阱但不能封路）
一般版：含繁體中文註解
"""

from __future__ import annotations

from collections import deque


def has_path(n: int, m: int, blocked: list[list[bool]]) -> bool:
    """檢查目前地圖是否仍存在從左側到右側的可行路徑。"""
    q: deque[tuple[int, int]] = deque()
    vis = [[False] * m for _ in range(n)]

    # 左側邊界作為多起點。
    for x in range(n):
        if not blocked[x][0]:
            vis[x][0] = True
            q.append((x, 0))

    if not q:
        return False

    while q:
        x, y = q.popleft()
        if y == m - 1:
            return True

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not blocked[nx][ny] and not vis[nx][ny]:
                vis[nx][ny] = True
                q.append((nx, ny))

    return False


def solve(text: str) -> str:
    vals = list(map(int, text.split()))
    if not vals:
        return ""

    i = 0
    n, m, t = vals[i], vals[i + 1], vals[i + 2]
    i += 3

    blocked = [[False] * m for _ in range(n)]
    out: list[str] = []

    for _ in range(t):
        x, y = vals[i], vals[i + 1]
        i += 2

        # 題目保證不重複放同一點，但仍保留安全檢查。
        if blocked[x][y]:
            out.append(">_<")
            continue

        blocked[x][y] = True
        if has_path(n, m, blocked):
            out.append("<(_ _)>")
        else:
            blocked[x][y] = False
            out.append(">_<")

    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
