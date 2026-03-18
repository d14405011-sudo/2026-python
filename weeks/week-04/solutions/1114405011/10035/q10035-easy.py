"""UVA 10035 - easy 版本（好記 + 繁體中文詳細註解）。

好記口訣：
1. 右邊一位一位相加。
2. 超過 9 就算一次進位。
3. 把進位帶到下一位。
4. 遇到 0 0 停止。
"""

import sys


def count_carries(a: int, b: int) -> int:
    # carries: 總進位次數
    carries = 0
    # carry: 當前要帶到下一位的進位值（只會是 0 或 1）
    carry = 0

    # 只要還有任一數字尚未處理，就持續逐位相加。
    while a > 0 or b > 0:
        # 取出個位數，再加上上一輪的進位。
        total = (a % 10) + (b % 10) + carry

        # 若總和 >= 10，代表本位發生進位。
        if total >= 10:
            carries += 1
            carry = 1
        else:
            carry = 0

        # 去掉已處理的個位數，進入下一位。
        a //= 10
        b //= 10

    return carries


def to_sentence(carries: int) -> str:
    # 依題目要求組出英文句型，注意 operation / operations 單複數。
    if carries == 0:
        return "No carry operation."
    if carries == 1:
        return "1 carry operation."
    return f"{carries} carry operations."


def solve(raw: str) -> str:
    ans = []

    # 題目是多行測資，直到出現 0 0 才結束。
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        x_str, y_str = line.split()
        x = int(x_str)
        y = int(y_str)

        # 終止條件：0 0 不輸出，直接停止。
        if x == 0 and y == 0:
            break

        ans.append(to_sentence(count_carries(x, y)))

    return "\n".join(ans) + ("\n" if ans else "")


def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
