"""UVA 10008 - Cryptanalysis 標準解法。

需求重點：
1. 大小寫視為同一字母。
2. 只統計英文字母 A~Z。
3. 先依次數遞減排序；次數相同依字母遞增排序。
"""

from collections import Counter
import sys


def solve(raw: str) -> str:
    lines = raw.splitlines()
    if not lines:
        return ""

    n = int(lines[0].strip())
    counter = Counter()

    for i in range(1, n + 1):
        line = lines[i] if i < len(lines) else ""
        for ch in line:
            up = ch.upper()
            if "A" <= up <= "Z":
                counter[up] += 1

    items = sorted(counter.items(), key=lambda it: (-it[1], it[0]))
    return "\n".join(f"{ch} {cnt}" for ch, cnt in items) + ("\n" if items else "")


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
