"""UVA 10908 - Largest Square

標準版解法：
- 以查詢中心往外擴張半徑。
- 每次擴張時檢查新正方形範圍內是否全部等於中心字元。
- 最大邊長 = 2 * 半徑 + 1。
"""

from __future__ import annotations


def is_valid_square(grid: list[str], r: int, c: int, radius: int, target: str) -> bool:
    """檢查以 (r, c) 為中心、半徑 radius 的正方形是否全部為 target。"""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    top = r - radius
    bottom = r + radius
    left = c - radius
    right = c + radius

    # 一旦超界，代表不能再擴張。
    if top < 0 or left < 0 or bottom >= rows or right >= cols:
        return False

    # 逐格確認是否都等於中心字元。
    for rr in range(top, bottom + 1):
        for cc in range(left, right + 1):
            if grid[rr][cc] != target:
                return False
    return True


def largest_square_size(grid: list[str], r: int, c: int) -> int:
    """回傳以 (r, c) 為中心的最大同字元正方形邊長（奇數）。"""
    target = grid[r][c]
    radius = 0

    # 從半徑 0 開始，不斷嘗試擴張到 1, 2, 3...
    while is_valid_square(grid, r, c, radius + 1, target):
        radius += 1

    return 2 * radius + 1


def solve_all(text: str) -> str:
    """依 UVA 輸入格式一次處理所有測資。"""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    idx = 0
    t = int(lines[idx])
    idx += 1

    out_lines: list[str] = []

    for _ in range(t):
        m, n, q = map(int, lines[idx].split())
        idx += 1

        grid = lines[idx : idx + m]
        idx += m

        out_lines.append(f"{m} {n} {q}")

        for _ in range(q):
            r, c = map(int, lines[idx].split())
            idx += 1
            out_lines.append(str(largest_square_size(grid, r, c)))

    return "\n".join(out_lines)


def main() -> None:
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
