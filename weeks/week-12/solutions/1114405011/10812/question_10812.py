"""UVA 10812 - Beat the Spread!
學號：1114405011

本檔案提供「標準版」解法，重點是把數學條件清楚封裝成函式，
讓主程式只負責讀取輸入與輸出結果，便於測試與重複使用。
"""

from __future__ import annotations

from typing import Optional, Tuple


def solve_case(total_score: int, diff_score: int) -> Optional[Tuple[int, int]]:
    """計算單一測資的兩隊分數。

    參數:
    - total_score: 兩隊分數總和 S
    - diff_score: 兩隊分數差 D（絕對值）

    回傳:
    - (high, low): 可行解，且 high >= low >= 0
    - None: 無解（例如奇偶不合、差大於和、或出現負數）

    數學推導:
    high = (S + D) / 2
    low  = (S - D) / 2

    合法條件:
    1) S + D 必須為偶數，否則 high 不是整數
    2) D <= S，否則 low 會是負數
    3) low >= 0（與條件 2 等價，但保留可讀性）
    """
    # 差比分數總和還大，代表低分會變負數，直接無解。
    if diff_score > total_score:
        return None

    # 只要 S + D 是奇數，就不可能得到整數分數。
    if (total_score + diff_score) % 2 != 0:
        return None

    high = (total_score + diff_score) // 2
    low = (total_score - diff_score) // 2

    # 理論上 diff_score <= total_score 已避免 low < 0，
    # 但這裡保留檢查，讓函式更健壯、更容易維護。
    if low < 0:
        return None

    return high, low


def format_result(total_score: int, diff_score: int) -> str:
    """把計算結果格式化成題目要求輸出的字串。"""
    result = solve_case(total_score, diff_score)
    if result is None:
        return "impossible"
    high, low = result
    return f"{high} {low}"


def main() -> None:
    """依題目 I/O 格式處理多組測資。"""
    n = int(input().strip())
    for _ in range(n):
        s_str, d_str = input().split()
        s = int(s_str)
        d = int(d_str)
        print(format_result(s, d))


if __name__ == "__main__":
    main()
