import sys


def solve(data):
    out = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        a, b = map(int, line.split())
        out.append(str(abs(a - b)))
    return "\n".join(out) + ("\n" if out else "")


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
import sys

def solve(data):
    out = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        a, b = map(int, line.split())
        out.append(str(abs(a - b)))
    return "\n".join(out) + ("\n" if out else "")

if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))