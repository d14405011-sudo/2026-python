import sys


def check(coin, heavy, ws):
    sign = 1 if heavy else -1
    for left, right, r in ws:
        d = (sign if coin in left else 0) - (sign if coin in right else 0)
        if r == "=" and d != 0:
            return False
        if r == "<" and d >= 0:
            return False
        if r == ">" and d <= 0:
            return False
    return True


def solve(data):
    tks = data.split()
    if not tks:
        return ""

    i = 0
    t = int(tks[i])
    i += 1
    out = []

    for _ in range(t):
        n = int(tks[i])
        k = int(tks[i + 1])
        i += 2
        ws = []
        genuine = set()
        suspicious = set()

        for _ in range(k):
            p = int(tks[i])
            i += 1
            left = list(map(int, tks[i:i + p]))
            i += p
            right = list(map(int, tks[i:i + p]))
            i += p
            r = tks[i]
            i += 1

            ws.append((left, right, r))
            involved = set(left) | set(right)
            if r == "=":
                genuine |= involved
            else:
                suspicious |= involved

        suspicious -= genuine

        if not suspicious:
            rem = [c for c in range(1, n + 1) if c not in genuine]
            out.append(str(rem[0] if len(rem) == 1 else 0))
            continue

        cand = []
        for c in sorted(suspicious):
            if check(c, True, ws) or check(c, False, ws):
                cand.append(c)

        out.append(str(cand[0] if len(cand) == 1 else 0))

    return "\n\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
import sys

def check(coin, heavy, ws):
    sign = 1 if heavy else -1
    for left, right, r in ws:
        d = (sign if coin in left else 0) - (sign if coin in right else 0)
        if r == "=" and d != 0:
            return False
        if r == "<" and d >= 0:
            return False
        if r == ">" and d <= 0:
            return False
    return True

def solve(data):
    tks = data.split()
    if not tks:
        return ""

    i = 0
    t = int(tks[i]); i += 1
    out = []

    for _ in range(t):
        n = int(tks[i]); k = int(tks[i + 1]); i += 2
        ws = []
        genuine = set()
        suspicious = set()

        for _ in range(k):
            p = int(tks[i]); i += 1
            left = list(map(int, tks[i:i + p])); i += p
            right = list(map(int, tks[i:i + p])); i += p
            r = tks[i]; i += 1

            ws.append((left, right, r))
            involved = set(left) | set(right)
            if r == "=":
                genuine |= involved
            else:
                suspicious |= involved

        suspicious -= genuine

        if not suspicious:
            rem = [c for c in range(1, n + 1) if c not in genuine]
            out.append(str(rem[0] if len(rem) == 1 else 0))
            continue

        cand = []
        for c in sorted(suspicious):
            if check(c, True, ws) or check(c, False, ws):
                cand.append(c)

        out.append(str(cand[0] if len(cand) == 1 else 0))

    return "\n\n".join(out) + "\n"

if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))