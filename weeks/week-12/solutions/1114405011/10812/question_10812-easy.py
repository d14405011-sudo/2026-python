"""UVA 10812 - Beat the Spread!（好記版 / easy）
學號：1114405011

這個版本刻意寫成「步驟化」流程：
1. 先做無解條件判斷
2. 再算大分與小分
3. 最後輸出

適合剛開始練習題目的同學，閱讀時只要記住一句口訣：
「先判斷、再計算、最後印」。
"""

from __future__ import annotations


def solve_one_case_easy(sum_score: int, gap_score: int) -> str:
    """回傳單筆測資的輸出字串。"""
    # 第 1 步：如果差比分數總和大，小分一定變負數，無解。
    if gap_score > sum_score:
        return "impossible"

    # 第 2 步：如果 sum + gap 是奇數，無法拆成兩個整數。
    if (sum_score + gap_score) % 2 == 1:
        return "impossible"

    # 第 3 步：依公式直接算。
    bigger = (sum_score + gap_score) // 2
    smaller = (sum_score - gap_score) // 2

    # 第 4 步：保險檢查（理論上前面條件已避免 smaller < 0）。
    if smaller < 0:
        return "impossible"

    return f"{bigger} {smaller}"


def main() -> None:
    """讀入多組資料並逐行輸出。"""
    test_count = int(input().strip())

    # 使用 for 迴圈跑完所有測資。
    for _ in range(test_count):
        total_text, diff_text = input().split()
        total = int(total_text)
        diff = int(diff_text)
        print(solve_one_case_easy(total, diff))


if __name__ == "__main__":
    main()
