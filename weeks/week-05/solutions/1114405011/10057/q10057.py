"""
UVA 10057 - The Lost Circle (密碼謎)
題目：找到最小化距離和的位置 A，輸出三個值

解題思路：
========
給定 n 個數字 x_1, x_2, ..., x_n
找到 A 使得 sum(|x_i - A|) 最小

輸出三個值：
1. A 的值（最優位置）
2. 最小值個數（有多少個 |x_i - A| 達到最小值）
3. 最優 A 的個數（有多少個不同的 A 能達到這個最小值）

分析：
- 奇數個數字：中位數是唯一最優解
- 偶數個數字：兩個中位數之間的所有整數都是最優解

特殊情況：
- 最小值個數：取決於最優解附近有多少個相同的數字
- 最優位置個數：
  - 奇數：1（只有中位數）
  - 偶數：upper_median - lower_median + 1
"""

def solve_q10057():
    """主程式：處理多組測試資料。"""
    while True:
        n = int(input())
        if n == 0:
            break

        numbers = [int(input()) for _ in range(n)]
        numbers.sort()

        if n % 2 == 1:
            # 奇數個：中位數唯一最優
            median = numbers[n // 2]
            min_values_count = numbers.count(median)
            optimal_positions = 1
            print(median, min_values_count, optimal_positions)
        else:
            # 偶數個：下中位數到上中位數都可行
            lower_median = numbers[n // 2 - 1]
            upper_median = numbers[n // 2]
            min_values_count = numbers.count(lower_median)
            optimal_positions = upper_median - lower_median + 1
            print(lower_median, min_values_count, optimal_positions)


if __name__ == "__main__":
    solve_q10057()
