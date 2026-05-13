"""UVA 10908 - Largest Square（好記版）

記憶口訣：
1. 取中心字元
2. 半徑從 0 往外加
3. 一圈不合法就停
"""

from __future__ import annotations


def largest_square_size_easy(grid: list[str], r: int, c: int) -> int:
    """較直觀版本：每擴張一層就完整掃描整個方形。"""
    ch = grid[r][c]
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    radius = 0
    while True:
        nr = radius + 1
        top = r - nr
        bottom = r + nr
        left = c - nr
        right = c + nr

        # 超出邊界就不能再擴張。
        if top < 0 or left < 0 or bottom >= rows or right >= cols:
            break

        ok = True
        for rr in range(top, bottom + 1):
            for cc in range(left, right + 1):
                if grid[rr][cc] != ch:
                    ok = False
                    break
            if not ok:
                break

        if not ok:
            break

        radius = nr

    return 2 * radius + 1


def solve_all_easy(text: str) -> str:
    """以簡單流程完成整體輸入輸出。"""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    i = 1
    out: list[str] = []

    for _ in range(t):
        m, n, q = map(int, lines[i].split())
        i += 1
        grid = lines[i : i + m]
        i += m

        out.append(f"{m} {n} {q}")

        for _ in range(q):
            r, c = map(int, lines[i].split())
            i += 1
            out.append(str(largest_square_size_easy(grid, r, c)))

    return "\n".join(out)


def main() -> None:
    import sys

    src = sys.stdin.read()
    res = solve_all_easy(src)
    if res:
        print(res)


if __name__ == "__main__":
    main()
