"""
UVA 10057 - The Lost Circle (詳細版本)

問題詳解：
========
科學家做夢看到很多數字 x_1, x_2, ..., x_n
需要找到一個整數 A 使得 sum(|x_i - A|) 最小

輸出三個值：
1. A 的值
2. 有多少個 |x_i - A| 達到最小值 min_value
3. 有多少個不同的 A 能達到這個最小值

關鍵概念：
=========

「最小值個數」vs「最優位置個數」的區別：
- 最小值個數：min_value = |x_1 - A| + |x_2 - A| + ... + |x_n - A|
  問的是：在最優位置上，有多少個 x_i 使得 |x_i - A| 恰好是最小距離？
  （通常是 1，除非有特殊情況）
  
- 最優位置個數：有多少個不同的 A 值都能達到相同的最小值

數學分析：
========

奇數個元素 n = 2k+1：
- 排序後中位數是 x_{k+1}（第 k+1 個）
- 任何其他位置 B ≠ x_{k+1} 都會增加距離和
- 只有中位數是最優解

偶數個元素 n = 2k：
- 排序後的下中位數是 x_k，上中位數是 x_{k+1}
- 對於任何 A ∈ [x_k, x_{k+1}]，距離和都相同
- A 的個數 = x_{k+1} - x_k + 1

例子：
====
[1, 2, 8, 9]（偶數個）
- 下中位數 = 2，上中位數 = 8
- A ∈ [2, 8] 都能達到最小值
- A 的個數 = 8 - 2 + 1 = 7
- 最小值個數通常是 1
"""

import sys

def solve_q10057_detailed():
    """
    詳細版本的 Q10057 解決方案
    """
    test_case = 0
    
    while True:
        n = int(input())
        
        if n == 0:
            break
        
        test_case += 1
        print(f"[測試 #{test_case}]", file=sys.stderr)
        print(f"  數字個數: {n}", file=sys.stderr)
        
        numbers = []
        for _ in range(n):
            numbers.append(int(input()))
        
        print(f"  原始數字: {numbers}", file=sys.stderr)
        
        # 排序
        numbers.sort()
        print(f"  排序後: {numbers}", file=sys.stderr)
        
        if n % 2 == 1:
            # 奇數個
            median = numbers[n // 2]
            print(f"  奇數個，中位數: {median}", file=sys.stderr)
            
            min_values_count = numbers.count(median)
            optimal_positions = 1
            
            print(f"  輸出: {median} {min_values_count} {optimal_positions}", file=sys.stderr)
            print(median, min_values_count, optimal_positions)
        
        else:
            # 偶數個
            lower_median = numbers[n // 2 - 1]
            upper_median = numbers[n // 2]
            
            print(f"  偶數個，下中位數: {lower_median}，上中位數: {upper_median}", file=sys.stderr)

            min_values_count = numbers.count(lower_median)
            optimal_positions = upper_median - lower_median + 1
            
            print(f"  最優位置數: {upper_median} - {lower_median} + 1 = {optimal_positions}",
                  file=sys.stderr)
            print(f"  輸出: {lower_median} {min_values_count} {optimal_positions}", file=sys.stderr)
            print(lower_median, min_values_count, optimal_positions)


if __name__ == "__main__":
    solve_q10057_detailed()
