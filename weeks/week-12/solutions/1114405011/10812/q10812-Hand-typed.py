def solve_case(s, d):
    if d > s:
        return None
    if (s + d) % 2 != 0:
        return None
    a = (s + d) // 2
    b = (s - d) // 2
    if b < 0:
        return None
    return a, b


def solve_all(text):
    lines = text.splitlines()
    if not lines:
        return ""
    t = int(lines[0].strip())
    out = []
    idx = 1
    for _ in range(t):
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        if idx >= len(lines):
            break
        s, d = map(int, lines[idx].split())
        idx += 1
        ans = solve_case(s, d)
        if ans is None:
            out.append("impossible")
        else:
            out.append(f"{ans[0]} {ans[1]}")
    return "\n".join(out)


def main():
    import sys

    src = sys.stdin.read()
    res = solve_all(src)
    if res:
        print(res)


if __name__ == "__main__":
    main()
