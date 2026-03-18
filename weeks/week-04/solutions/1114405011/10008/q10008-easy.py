"""UVA 10008 - easy 版本（好記憶 + 繁體中文詳細註解）。

口訣四步驟：
1. 讀 n 行。
2. 只抓字母，全部轉大寫來統計。
3. 排序規則：次數大到小，字母小到大。
4. 逐行輸出「字母 次數」。
"""

import sys


def solve(raw: str) -> str:
    # splitlines() 會保留「每一行」的概念，空行也能正常處理。
    lines = raw.splitlines()
    if not lines:
        return ""

    # 第 1 行是要分析的行數 n。
    n = int(lines[0].strip())

    # 用 dict 做次數表，key 是大寫字母，value 是出現次數。
    freq = {}

    # 從第 2 行開始，總共處理 n 行密文。
    for i in range(1, n + 1):
        # 如果輸入行數不足，缺的行就當空字串處理，避免索引錯誤。
        line = lines[i] if i < len(lines) else ""

        # 掃描每個字元，只統計英文字母。
        for ch in line:
            up = ch.upper()
            if "A" <= up <= "Z":
                freq[up] = freq.get(up, 0) + 1

    # 排序規則：
    # 1) -count => 次數多的在前面
    # 2) letter => 次數相同時，字母序小的在前面
    pairs = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

    # 組出題目要求格式：每行 "字母 次數"
    out_lines = [f"{letter} {count}" for letter, count in pairs]

    # UVA/ZeroJudge 習慣輸出最後保留換行。
    return "\n".join(out_lines) + ("\n" if out_lines else "")


def main() -> None:
    # 從標準輸入讀整份資料後，交給 solve() 處理。
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
