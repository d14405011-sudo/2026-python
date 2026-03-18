"""UVA 10019（依題面描述版本）標準解法。

題意（依目前題面）：
- 每行輸入兩個整數。
- 對每行輸出兩數的絕對差值。
"""

import sys


def solve(raw: str) -> str:
    outputs = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        a_str, b_str = line.split()
        a = int(a_str)
        b = int(b_str)
        outputs.append(str(abs(a - b)))

    return "\n".join(outputs) + ("\n" if outputs else "")


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
