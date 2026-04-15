"""
UVA 10222 - Decode the Mad man

常見解法：
- 依鍵盤每一列建立對照表，略過每列最左邊沒有更左側按鍵可對應的字元。
- 瘋子打字時手往右偏，解碼時把每個字元映射到左邊第 1 個按鍵。
"""

ROWS = [
    "`1234567890-=",
    "QWERTYUIOP[]\\",
    "ASDFGHJKL;'",
    "ZXCVBNM,./",
]


def build_map() -> dict[str, str]:
    """建立解碼映射表（同時支援大小寫）。"""
    mp: dict[str, str] = {}
    for row in ROWS:
        for i in range(1, len(row)):
            mp[row[i]] = row[i - 1]
            if row[i].isalpha():
                mp[row[i].lower()] = row[i - 1].lower()
    return mp


DECODE_MAP = build_map()


def decode_line(line: str) -> str:
    """解碼單行文字。"""
    return "".join(DECODE_MAP.get(ch, ch) for ch in line)


def solve_all(text: str) -> str:
    lines = text.splitlines()
    return "\n".join(decode_line(line) for line in lines)


def main() -> None:
    import sys

    src = sys.stdin.read()
    if not src:
        return
    print(solve_all(src))


if __name__ == "__main__":
    main()
