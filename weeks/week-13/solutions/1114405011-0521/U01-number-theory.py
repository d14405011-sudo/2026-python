# U01. 數論整合應用
# 這份教材示範如何把「數學觀念」轉成「可執行程式」：
# 1) 由和差反推兩個整數（線性方程組）
# 2) 使用數位和判斷 9 的倍數（大數字串處理）
# 3) 以公式映射座標到編號（避免逐步模擬）
#
# 注意：本檔案以教學清楚為優先，因此搭配較多中文註解。
# 執行時會直接印出三個題型的示範結果。

import math
import sys

# ── 應用 1：Beat the Spread!（UVA 10812）────────────────
# 題意：
# 已知兩隊比分總和 S、分差 D，求高分隊與低分隊各得幾分。
#
# 由聯立方程可得：
#   high + low = S
#   high - low = D
# 兩式相加、相減後得到：
#   high = (S + D) / 2
#   low  = (S - D) / 2
#
# 合法答案必須同時滿足：
# 1) (S + D) 為偶數（否則除以 2 後不是整數）
# 2) low >= 0（分數不可為負）

def beat_the_spread(s: int, d: int):
    """
    根據總和 s 與分差 d，回傳 (高分, 低分) 或 None（無解）。

    參數：
    - s: 兩隊總分
    - d: 兩隊分差（高分 - 低分）

    回傳：
    - tuple[int, int]: (high, low)
    - None: 代表無合法整數解

    判斷重點：
    - 若 s+d 為奇數，high 不是整數，直接無解。
    - 若 low < 0，代表低分為負，也無解。
    """
    # high = (s + d) / 2 若不是整數，題目要求的整數比分不存在。
    if (s + d) % 2 != 0:
        return None

    # 使用整數除法計算兩隊分數。
    high = (s + d) // 2
    low  = (s - d) // 2

    # 低分若小於 0，代表分數組合不合理（例如分差大於總分）。
    if low < 0:
        return None
    return (high, low)


print("=== Beat the Spread! ===")
tests = [(40, 20), (20, 40), (10, 10), (10, 11)]
for s, d in tests:
    result = beat_the_spread(s, d)
    if result:
        print(f"S={s} D={d}  → {result[0]} {result[1]}")
    else:
        print(f"S={s} D={d}  → impossible")

# ── 應用 2：2 the 9s（UVA 10922）────────────────────────
# 題意：
# 給一個很大的整數（以字串提供），判斷是否為 9 的倍數；
# 若是，還要回傳它的 9-degree（反覆做「各位數字總和」直到變成 9 的層數）。
#
# 例：999 -> 27 -> 9，因此 degree = 3。
#
# 為何可行：
# 一個數是否為 9 的倍數，等價於其各位數字和是否為 9 的倍數。
# 這讓我們可以處理超過 int 範圍的大數字串。
def nine_degree(n_str: str):
    """
    計算數字字串是否為 9 的倍數，並回傳其 9-degree。

    參數：
    - n_str: 數字字串（可非常大）

    回傳：
    - (True, degree): 為 9 的倍數，且 degree 為轉換層數
    - (False, -1): 不是 9 的倍數

    實作細節：
    - 每一輪把 current 的所有字元轉成數字後加總。
    - degree 記錄「做了幾輪數位和」。
    - 最終若收斂到單一數字 9，代表是 9 的倍數。
    """
    current = n_str
    degree = 0

    # 至少要做一輪（即使輸入本來就是單一數字），
    # 才能正確定義像 "9" 的 degree = 1。
    while len(current) > 1 or (degree == 0 and len(current) == 1):
        # 以字串逐字元處理，避免大數轉型溢位問題。
        s = sum(int(c) for c in current)
        current = str(s)
        degree += 1

        # 已縮成個位數可提早結束，節省不必要迴圈。
        if len(current) == 1:
            break

    # 最後單一數字若為 9，表示原數是 9 的倍數。
    if current == "9":
        return True, degree
    return False, -1


print("\n=== 2 the 9s ===")
cases = ["9", "18", "999", "100", "729"]
for n in cases:
    is_mult, deg = nine_degree(n)
    if is_mult:
        print(f"9-degree of {n} is {deg}.")
    else:
        print(f"{n} is not a multiple of 9.")

# ── 應用 3：Can You Solve It?（UVA 10642）────────────────
# 題意：
# 座標點依特定規則沿對角線編號，要求兩點之間相差幾步。
#
# 關鍵想法：
# 不要真的一格一格走，直接把 (x, y) 映射到其編號 position，
# 兩點步數就是編號差的絕對值。
#
# 公式（依 x 與 y 的大小分段）：
# - 若 x >= y: position = x^2 + x + y
# - 若 x <  y: position = y^2 + x
#
# 這是題目座標排列規則推導出的 closed-form，時間複雜度 O(1)。

def position(x, y):
    """
    計算座標 (x, y) 在題目序列中的位置編號（從 0 開始）。

    參數：
    - x, y: 非負整數座標

    回傳：
    - int: 對應的序列編號
    """
    # x >= y 與 x < y 分屬於不同對角帶，使用對應公式。
    if x >= y:
        return x * x + x + y
    else:
        return y * y + x

def steps(x1, y1, x2, y2):
    """
    回傳兩座標在此編號系統中的步數差。

    因為每前進一格對應編號 +1，
    所以步數 = |position(B) - position(A)|。
    """
    return abs(position(x2, y2) - position(x1, y1))


print("\n=== Can You Solve It? ===")
cases = [(0, 3, 3, 0), (0, 0, 2, 2), (1, 1, 2, 3)]
for x1, y1, x2, y2 in cases:
    s = steps(x1, y1, x2, y2)
    print(f"({x1},{y1}) → ({x2},{y2})  步數 = {s}")
