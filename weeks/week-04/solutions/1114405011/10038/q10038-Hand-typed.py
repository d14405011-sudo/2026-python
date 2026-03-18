import sys


def is_jolly(seq):
    n = len(seq)
    if n <= 1:
        return True

    seen = set()
    for i in range(1, n):
        d = abs(seq[i] - seq[i - 1])
        if d < 1 or d >= n:
            return False
        seen.add(d)

    return len(seen) == n - 1


def solve(data):
    out = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        nums = list(map(int, line.split()))
        n = nums[0]
        seq = nums[1:1 + n]
        out.append("Jolly" if is_jolly(seq) else "Not jolly")
    return "\n".join(out) + ("\n" if out else "")


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
