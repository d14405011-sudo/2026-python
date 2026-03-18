"""q10019 easy 版本（好記 + 繁體中文詳細註解）。

記憶口訣：
1. 一行一組資料。
2. 兩個數字相減取絕對值。
3. 每組結果印一行。
"""

import sys


def solve(raw: str) -> str:
    # 用來收集每一組測資的答案字串。
    ans = []

    # 題目是讀到 EOF，所以把所有行逐一掃過。
    for line in raw.splitlines():
        # 先去除前後空白，避免多餘空白造成 split 問題。
        line = line.strip()

        # 空行直接跳過，不算測資。
        if not line:
            continue

        # 每行有兩個整數（Hashmat 與敵軍，或反過來）。
        x_str, y_str = line.split()
        x = int(x_str)
        y = int(y_str)

        # 題目要求輸出正差值，所以使用 abs()。
        ans.append(str(abs(x - y)))

    # 題目輸出慣例：有內容時最後保留換行。
    return "\n".join(ans) + ("\n" if ans else "")


def main() -> None:
    # 從標準輸入讀到 EOF，交給 solve() 處理。
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
