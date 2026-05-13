def largest_square_size(grid, r, c):
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


def solve_all(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    if not lines:
        return ""
    t = int(lines[0])
    i = 1
    out = []
    for _ in range(t):
        m, n, q = map(int, lines[i].split())
        i += 1
        g = lines[i:i + m]
        i += m
        out.append(f"{m} {n} {q}")
        for _ in range(q):
            r, c = map(int, lines[i].split())
            i += 1
            out.append(str(largest_square_size(g, r, c)))
    return "\n".join(out)


def main():
    import sys

    s = sys.stdin.read()
    a = solve_all(s)
    if a:
        print(a)


if __name__ == "__main__":
    main()
