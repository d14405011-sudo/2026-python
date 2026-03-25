"""
UVA 10041 - Vito's Family (詳細版本)

問題分析：
========
Vito 需要找到一個位置，使得到所有親戚房子的距離和最小。
這是一個經典的「1維最小化距離和」問題，答案是中位數。

為什麼是中位數？
===============
設所有房子位置為 [a₁, a₂, ..., aₙ]，選擇位置 x
距離函數 D(x) = |a₁-x| + |a₂-x| + ... + |aₙ-x|

對 D(x) 求導（在連續情況下）：
- 當 x 在中位數左邊時，D'(x) < 0（遞減）
- 當 x 在中位數右邊時，D'(x) > 0（遞增）
- 因此中位數是最小值點

特殊情況：
========
1. 奇數個親戚：取中間的值作為中位數
2. 偶數個親戚：取中間兩個值的任意一個都是最優解

時間複雜度：O(n log n) - 排序
空間複雜度：O(n)
"""

def solve_q10041_detailed():
    """
    詳細版本的 Q10041 解決方案
    包含完整的演算法說明和測試輸出
    """
    t = int(input())  # 讀取測試資料組數
    
    for test_case in range(1, t + 1):
        line = list(map(int, input().split()))
        r = line[0]
        relatives = line[1:r+1]
        
        print(f"[測試 #{test_case}]", file=__import__('sys').stderr)
        print(f"  親戚數: {r}", file=__import__('sys').stderr)
        print(f"  原始位置: {relatives}", file=__import__('sys').stderr)
        
        # 步驟 1：排序親戚的房子位置
        relatives.sort()
        print(f"  排序後: {relatives}", file=__import__('sys').stderr)
        
        # 步驟 2：計算中位數
        n = len(relatives)
        if n % 2 == 1:
            # 奇數個親戚
            median_idx = n // 2
            median = relatives[median_idx]
            print(f"  奇數個親戚，中位數索引: {median_idx}，值: {median}", file=__import__('sys').stderr)
        else:
            # 偶數個親戚
            median_idx = n // 2 - 1
            median = relatives[median_idx]
            print(f"  偶數個親戚，下中位數索引: {median_idx}，值: {median}", file=__import__('sys').stderr)
        
        # 步驟 3：計算距離和
        distances = [abs(h - median) for h in relatives]
        total_distance = sum(distances)
        
        print(f"  每個親戚的距離: {distances}", file=__import__('sys').stderr)
        print(f"  距離總和: {total_distance}", file=__import__('sys').stderr)
        
        # 輸出答案
        print(total_distance)


if __name__ == "__main__":
    solve_q10041_detailed()
