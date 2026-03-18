"""UVA 10038 - Jolly Jumpers 標準解法。

判斷規則：
- 長度為 n 的序列，計算相鄰差絕對值。
- 若差值集合剛好包含 1..n-1，則是 Jolly，否則 Not jolly。
"""

import sys


def is_jolly(seq):
    """判斷單一序列是否為 jolly jumper。"""

    n = len(seq)
    if n <= 1:
        return True

    diffs = set()
    for i in range(1, n):
        d = abs(seq[i] - seq[i - 1])
        if d < 1 or d >= n:
            return False
        diffs.add(d)

    return len(diffs) == n - 1


def solve(raw: str) -> str:
    outputs = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        nums = list(map(int, line.split()))
        n = nums[0]
        seq = nums[1:1 + n]
        outputs.append("Jolly" if is_jolly(seq) else "Not jolly")

    return "\n".join(outputs) + ("\n" if outputs else "")


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
