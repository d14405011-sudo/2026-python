def parity_line(n):
    b = bin(n)[2:]
    p = b.count("1")
    return f"The parity of {b} is {p} (mod 2)."


def solve_all(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        v = int(s)
        if v == 0:
            break
        out.append(parity_line(v))
    return "\n".join(out)


def main():
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
