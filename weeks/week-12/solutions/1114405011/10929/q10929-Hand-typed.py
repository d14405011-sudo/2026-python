def is_multiple_of_11(s):
    rem = 0
    for ch in s:
        rem = (rem * 10 + int(ch)) % 11
    return rem == 0


def solve_all(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s == "0":
            break
        if is_multiple_of_11(s):
            out.append(f"{s} is a multiple of 11.")
        else:
            out.append(f"{s} is not a multiple of 11.")
    return "\n".join(out)


def main():
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
