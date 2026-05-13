def digit_sum(s):
    return sum(int(ch) for ch in s)


def nine_degree(s):
    if s == "9":
        return 1
    x = digit_sum(s)
    if x % 9 != 0:
        return None
    d = 1
    while x > 9:
        x = digit_sum(str(x))
        d += 1
    if x == 9:
        return d
    return None


def solve_all(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s == "0":
            break
        d = nine_degree(s)
        if d is None:
            out.append(f"{s} is not a multiple of 9.")
        else:
            out.append(f"9-degree of {s} is {d}.")
    return "\n".join(out)


def main():
    import sys

    src = sys.stdin.read()
    ans = solve_all(src)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
