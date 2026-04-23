"""
UVA 10189 - Minesweeper（easy 版）

易記版本：
- 先在地圖外圍補一圈 '.'。
- 這樣每格都可直接掃 3x3，不用寫邊界判斷。
"""


def solve_field(grid: list[str]) -> list[str]:
    n = len(grid)
    m = len(grid[0]) if n else 0

    padded = [['.'] * (m + 2)]
    for row in grid:
        padded.append(['.'] + list(row) + ['.'])
    padded.append(['.'] * (m + 2))

    out: list[str] = []
    for r in range(1, n + 1):
        row = []
        for c in range(1, m + 1):
            if padded[r][c] == '*':
                row.append('*')
            else:
                cnt = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        if padded[r + dr][c + dc] == '*':
                            cnt += 1
                row.append(str(cnt))
        out.append(''.join(row))
    return out


def solve_all(text: str) -> str:
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

        grid = [lines[idx + i] for i in range(n)]
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
