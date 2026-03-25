"""
UVA 10041 - Vito's Family
題目：找到距離所有親戚房子總距離最小的位置

解題思路：
中位數問題 - 在一維直線上，中位數位置使得到所有點的距離和最小。
このロジックは、距離の合計が中位數でのみ最小化されるという數學的性質に基づいています。

輸入：
- 第一行：測試資料組數 t
- 每組資料第一行：親戚數 r 和 r 個親戚的房子門牌號碼

輸出：
- 距離總和的最小值
"""

def solve_q10041():
    """
    主程式：讀取輸入並計算每組測試資料
    """
    t = int(input())  # 讀取測試資料組數
    for _ in range(t):
        line = list(map(int, input().split()))  # 讀取一行資料
        r = line[0]  # 親戚數
        relatives = line[1:r+1]  # 親戚的房子門牌號碼
        
        # 對所有門牌號碼排序
        relatives.sort()
        
        # 取中位數作為最優位置
        # 奇數個親戚時取中間值，偶數個親戚時取下中位數
        if len(relatives) % 2 == 1:
            median = relatives[len(relatives) // 2]
        else:
            median = relatives[len(relatives) // 2 - 1]
        
        # 計算從中位數位置到所有親戚房子的距離總和
        total_distance = sum(abs(house - median) for house in relatives)
        
        # 輸出結果
        print(total_distance)


if __name__ == "__main__":
    solve_q10041()
