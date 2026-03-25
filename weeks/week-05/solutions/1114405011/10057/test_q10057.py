"""
UVA 10057 - The Lost Cricle (密碼謎) 測試程式
題目：找到最小化距離和的位置，並計算滿足條件的位置和方案數
"""

import unittest
from io import StringIO
import sys


def solve_q10057():
    """
    解決 UVA 10057 - 密碼謎
    """
    while True:
        try:
            n = int(input())
            if n == 0:
                break
            
            numbers = []
            for _ in range(n):
                numbers.append(int(input()))
            
            if n == 0:
                continue
            
            # 排序
            numbers.sort()
            
            # 找到最優位置
            if n % 2 == 1:
                # 奇數個，中位數是唯一最優解
                median = numbers[n // 2]
                min_sum = sum(abs(x - median) for x in numbers)
                
                # 計算有多少個數字等於中位數（這些是達到最小距離的數字）
                min_values_count = numbers.count(median)
                
                # 最優位置的個數
                optimal_positions = 1
                
                print(median, min_values_count, optimal_positions)
            else:
                # 偶數個，兩個中位數之間的所有整數都是最優解
                lower_median = numbers[n // 2 - 1]
                upper_median = numbers[n // 2]
                
                # 計算最小距離和
                min_sum = sum(abs(x - lower_median) for x in numbers)
                
                # 最小值的個數
                min_values_count = numbers.count(lower_median)
                
                # 最優位置的個數
                optimal_positions = upper_median - lower_median + 1
                
                print(lower_median, min_values_count, optimal_positions)
        
        except EOFError:
            break


class TestQ10057(unittest.TestCase):
    """Q10057 的單元測試"""
    
    def solve_with_input(self, input_str):
        """
        模擬輸入並執行程式
        """
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = StringIO(input_str)
        sys.stdout = StringIO()
        
        try:
            solve_q10057()
            output = sys.stdout.getvalue()
            return output.strip()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
    
    def test_odd_numbers(self):
        """測試奇數個數字"""
        input_data = """3
1
3
5
0"""
        # 中位數是 3，距離和 = |1-3| + |3-3| + |5-3| = 2 + 0 + 2 = 4
        # 最小值個數：1（只有一個 3 達到 0）
        # 最優位置個數：1（只有 3）
        result = self.solve_with_input(input_data).split('\n')[0]
        parts = result.split()
        self.assertEqual(parts[0], "3")
        self.assertEqual(parts[1], "1")
        self.assertEqual(parts[2], "1")
    
    def test_even_numbers(self):
        """測試偶數個數字"""
        input_data = """4
1
2
8
9
0"""
        # 中位數是 2 和 8，所以 A 可以是 2, 3, ..., 8
        # 距離和 = |1-2| + |2-2| + |8-2| + |9-2| = 1 + 0 + 6 + 7 = 14
        # 最小值個數：1（只有一個 2 達到 0）
        # 最優位置個數：7（2 到 8 的整數）
        result = self.solve_with_input(input_data).split('\n')[0]
        parts = result.split()
        self.assertEqual(parts[0], "2")
        self.assertEqual(parts[1], "1")
        self.assertEqual(parts[2], "7")
    
    def test_duplicate_numbers(self):
        """測試有重複的數字"""
        input_data = """4
5
5
5
5
0"""
        # 所有都是 5，中位數是 5
        # 距離和 = 0
        # 最小值個數：4（所有 5 都達到 0）
        # 最優位置個數：1
        result = self.solve_with_input(input_data).split('\n')[0]
        parts = result.split()
        self.assertEqual(parts[0], "5")
        self.assertEqual(parts[1], "4")  # 有 4 個 5
        self.assertEqual(parts[2], "1")  # 只有一個最優位置


if __name__ == '__main__':
    unittest.main()
