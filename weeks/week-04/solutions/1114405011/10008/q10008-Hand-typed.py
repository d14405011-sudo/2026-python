import sys


def solve(data):
    lines = data.splitlines()
    if not lines:
        return ""

    n = int(lines[0].strip())
    freq = {}

    for i in range(1, n + 1):
        line = lines[i] if i < len(lines) else ""
        for ch in line:
            up = ch.upper()
            if "A" <= up <= "Z":
                freq[up] = freq.get(up, 0) + 1

    items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return "\n".join(f"{c} {k}" for c, k in items) + ("\n" if items else "")


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
import sys

def solve(data):
    lines = data.splitlines()
    if not lines:
        return ""

    n = int(lines[0].strip())
    freq = {}

    for i in range(1, n + 1):
        line = lines[i] if i < len(lines) else ""
        for ch in line:
            up = ch.upper()
            if "A" <= up <= "Z":
                freq[up] = freq.get(up, 0) + 1

    items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return "\n".join(f"{c} {k}" for c, k in items) + ("\n" if items else "")

if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))