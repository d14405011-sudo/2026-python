"""UVA 10038 - easy 版本（好記 + 繁體中文詳細註解）。

記憶口訣：
1. 算相鄰兩數的差絕對值。
2. 差值必須都在 1..n-1。
3. 且不能重複、總共要有 n-1 個。
4. 符合就是 Jolly，否則 Not jolly。
"""

import sys


def is_jolly(seq):
    # n 是序列長度。
    n = len(seq)

    # 長度 0 或 1，沒有相鄰差可檢查，視為 Jolly。
    if n <= 1:
        return True

    # 用集合收集差值，可自動去重複。
    seen = set()

    for i in range(1, n):
        # 計算相鄰兩數差的絕對值。
        d = abs(seq[i] - seq[i - 1])

        # 若差值不在合法範圍，直接失敗。
        if d < 1 or d >= n:
            return False

        seen.add(d)

    # 必須剛好收集到 n-1 個不同差值。
    return len(seen) == n - 1


def solve(raw: str) -> str:
    ans = []

    # 題目是逐行測資直到 EOF。
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        nums = list(map(int, line.split()))
        n = nums[0]
        seq = nums[1:1 + n]

        if is_jolly(seq):
            ans.append("Jolly")
        else:
            ans.append("Not jolly")

    return "\n".join(ans) + ("\n" if ans else "")


def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
