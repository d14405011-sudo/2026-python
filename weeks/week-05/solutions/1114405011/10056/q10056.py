"""
UVA 10056 - Dice (骰子)
題目：計算指定玩家的獲勝機率

解題思路：
========
N 個玩家輪流扔骰子，每次成功機率為 p
如何計算第 i 個玩家的獲勝機率？

分析：
第 i 個玩家在第一輪獲勝的機率：
- 前 i-1 個玩家都失敗：(1-p)^(i-1)
- 第 i 個玩家成功：p
- 小計：p × (1-p)^(i-1)

第 i 個玩家在第二輪獲勝的機率：
- 第一輪沒有人成功：(1-p)^N
- 前 i-1 個玩家失敗：(1-p)^(i-1)
- 第 i 個玩家成功：p
- 小計：p × (1-p)^N × (1-p)^(i-1)

第 i 個玩家在第 k 輪獲勝的機率：
- p × (1-p)^(N(k-1)) × (1-p)^(i-1)

總機率（無限級數）：
P_i = p × (1-p)^(i-1) × [1 + (1-p)^N + (1-p)^(2N) + ...]
    = p × (1-p)^(i-1) × 1 / (1 - (1-p)^N)

其中 (1-p)^N < 1，級數收斂
"""

def solve_q10056():
    """
    主程式：讀取輸入並計算獲勝機率
    """
    s = int(input())  # 測試資料組數
    
    for _ in range(s):
        n, p, i = map(float, input().split())
        n = int(n)
        i = int(i)
        
        # 計算第 i 個玩家的獲勝機率
        # 公式：P_i = p × (1-p)^(i-1) / (1 - (1-p)^n)
        
        numerator = p * ((1 - p) ** (i - 1))  # 分子
        denominator = 1 - ((1 - p) ** n)       # 分母
        
        probability = numerator / denominator
        
        # 輸出四位小數
        print(f"{probability:.4f}")


if __name__ == "__main__":
    solve_q10056()
