"""
UVA 10056 - Dice (詳細版本)

機率推導詳解：
=============

情況設定：
- N 個玩家 (編號 1 到 N)
- 輪流扔骰子，順序為 1, 2, ..., N, 1, 2, ...
- 每次成功機率為 p
- 第一次成功的人獲勝

求：第 i 個玩家的獲勝機率 P_i

推導過程：
========

定義 q = 1 - p（失敗機率）

第 1 輪（第 1 到 N 個玩家各一次），玩家 i 獲勝的條件：
- 玩家 1 到 i-1 都失敗：q^(i-1)
- 玩家 i 成功：p
- 機率：p × q^(i-1)

第 2 輪玩家 i 獲勝的條件：
- 第 1 輪沒人成功：q^N
- 玩家 1 到 i-1 失敗：q^(i-1)
- 玩家 i 成功：p
- 機率：p × q^N × q^(i-1)

第 k 輪玩家 i 獲勝的條件：
- 前 k-1 輪沒人成功：q^(N(k-1))
- 玩家 1 到 i-1 失敗：q^(i-1)
- 玩家 i 成功：p
- 機率：p × q^(N(k-1)) × q^(i-1)

總機率（所有輪）：
P_i = Σ(k=1 to ∞) p × q^(N(k-1)) × q^(i-1)
    = p × q^(i-1) × Σ(k=1 to ∞) q^(N(k-1))
    = p × q^(i-1) × Σ(k=0 to ∞) (q^N)^k
    = p × q^(i-1) × 1 / (1 - q^N)    [幾何級數，|q^N| < 1]
    = p × (1-p)^(i-1) / (1 - (1-p)^N)

例子：
====
正常骰子（6面）有 1/6 機率獲得特定數字
若有 3 個玩家，p = 1/6
P_1 = (1/6) × (5/6)^0 / (1 - (5/6)^3)
    = (1/6) / (1 - 125/216)
    = (1/6) / (91/216)
    ≈ 0.3976
"""

import sys

def solve_q10056_detailed():
    """
    詳細版本的 Q10056 解決方案
    """
    s = int(input())
    
    for test_idx in range(1, s + 1):
        n, p, i = map(float, input().split())
        n = int(n)
        i = int(i)
        
        print(f"[測試 #{test_idx}]", file=sys.stderr)
        print(f"  玩家數 N = {n}", file=sys.stderr)
        print(f"  成功機率 p = {p}", file=sys.stderr)
        print(f"  查詢玩家 i = {i}", file=sys.stderr)
        
        q = 1 - p  # 失敗機率
        print(f"  失敗機率 q = {q}", file=sys.stderr)
        
        # 計算分子：p × q^(i-1)
        numerator = p * (q ** (i - 1))
        print(f"  分子 = p × q^(i-1) = {p} × {q}^{i-1} = {numerator}", file=sys.stderr)
        
        # 計算分母：1 - q^N
        denominator = 1 - (q ** n)
        print(f"  分母 = 1 - q^N = 1 - {q}^{n} = {denominator}", file=sys.stderr)
        
        # 計算機率
        probability = numerator / denominator
        print(f"  獲勝機率 = {numerator} / {denominator} = {probability}", file=sys.stderr)
        print(f"  輸出（四捨五入至四位小數）: {probability:.4f}", file=sys.stderr)
        
        print(f"{probability:.4f}")


if __name__ == "__main__":
    solve_q10056_detailed()
