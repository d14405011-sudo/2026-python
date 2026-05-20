from __future__ import annotations

from collections import deque


def chk(n: int, m: int, b: list[list[bool]]) -> bool:
    q: deque[tuple[int, int]] = deque()
    v = [[False] * m for _ in range(n)]

    for x in range(n):
        if not b[x][0]:
            v[x][0] = True
            q.append((x, 0))

    while q:
        x, y = q.popleft()
        if y == m - 1:
            return True

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not b[nx][ny] and not v[nx][ny]:
                v[nx][ny] = True
                q.append((nx, ny))

    return False


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    if not a:
        return ""

    n, m, t = a[0], a[1], a[2]
    i = 3

    b = [[False] * m for _ in range(n)]
    out: list[str] = []

    for _ in range(t):
        x, y = a[i], a[i + 1]
        i += 2

        b[x][y] = True
        if chk(n, m, b):
            out.append("<(_ _)>")
        else:
            b[x][y] = False
            out.append(">_<")

    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
