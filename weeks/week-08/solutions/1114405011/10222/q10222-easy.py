"""
UVA 10222 - easy 版

易記法：
- 用一條鍵盤字串。
- 字元位置往左退 2。
"""

ROWS = [
    "`1234567890-=",
    "QWERTYUIOP[]\\",
    "ASDFGHJKL;'",
    "ZXCVBNM,./",
]

M = {}
for row in ROWS:
    for i in range(1, len(row)):
        M[row[i]] = row[i - 1]
        if row[i].isalpha():
            M[row[i].lower()] = row[i - 1].lower()


def decode_line(line: str) -> str:
    return "".join(M.get(ch, ch) for ch in line)


def solve_all(text: str) -> str:
    return "\n".join(decode_line(x) for x in text.splitlines())


def main() -> None:
    import sys

    data = sys.stdin.read()
    if data:
        print(solve_all(data))


if __name__ == "__main__":
    main()
