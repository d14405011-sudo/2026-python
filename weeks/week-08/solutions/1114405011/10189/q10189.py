"""
UVA 10189 - Minesweeper

解法重點：
1. 逐格掃描地圖。
2. 若是地雷保留 '*'。
3. 若是空格，檢查周圍 8 個方向並計算地雷數。
"""

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def solve_field(grid: list[str]) -> list[str]:
    """將單一地雷圖轉換成題目要求的數字圖。"""
    n = len(grid)
    m = len(grid[0]) if n else 0
    out: list[str] = []

    for r in range(n):
        row = []
        for c in range(m):
            if grid[r][c] == '*':
                row.append('*')
                continue

            mines = 0
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == '*':
                    mines += 1
            row.append(str(mines))
        out.append(''.join(row))

    return out


def solve_all(text: str) -> str:
    """處理多組輸入並回傳完整輸出字串。"""
    lines = text.splitlines()
    idx = 0
    case_no = 0
    blocks: list[str] = []

    while idx < len(lines):
        line = lines[idx].strip()
        idx += 1
        if not line:
            continue

        n, m = map(int, line.split())
        if n == 0 and m == 0:
            break

        grid = [lines[idx + i].rstrip('\n') for i in range(n)]
        idx += n

        case_no += 1
        block = [f"Field #{case_no}:"]
        block.extend(solve_field(grid))
        blocks.append('\n'.join(block))

    return '\n\n'.join(blocks)


def main() -> None:
    import sys

    data = sys.stdin.read()
    ans = solve_all(data)
    if ans:
        print(ans)


if __name__ == '__main__':
    main()
