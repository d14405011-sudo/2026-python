"""UVA 10035 - Primary Arithmetic 標準解法。

題意：
- 每行給兩個整數，計算直式加法會產生幾次進位。
- 遇到 `0 0` 結束輸入。
"""

import sys


def count_carries(a: int, b: int) -> int:
    """回傳 a+b 在逐位相加時的進位次數。"""

    carries = 0
    carry = 0

    while a > 0 or b > 0:
        digit_sum = (a % 10) + (b % 10) + carry
        if digit_sum >= 10:
            carries += 1
            carry = 1
        else:
            carry = 0

        a //= 10
        b //= 10

    return carries


def format_result(carries: int) -> str:
    """依題目格式輸出英文句子。"""

    if carries == 0:
        return "No carry operation."
    if carries == 1:
        return "1 carry operation."
    return f"{carries} carry operations."


def solve(raw: str) -> str:
    outputs = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        a_str, b_str = line.split()
        a = int(a_str)
        b = int(b_str)

        if a == 0 and b == 0:
            break

        outputs.append(format_result(count_carries(a, b)))

    return "\n".join(outputs) + ("\n" if outputs else "")


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
