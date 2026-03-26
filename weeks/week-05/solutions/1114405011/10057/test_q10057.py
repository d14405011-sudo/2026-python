"""
UVA 10057 - The Lost Circle (密碼謎) 測試程式
題目：找到最小化距離和的位置，並計算滿足條件的位置和方案數
"""

import unittest
from io import StringIO
import sys
from q10057 import solve_q10057
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
        # 介於兩個中位數 [2, 8] 的輸入數字個數：2（2 與 8）
        # 最優位置個數：7（2 到 8 的整數）
        result = self.solve_with_input(input_data).split('\n')[0]
        parts = result.split()
        self.assertEqual(parts[0], "2")
        self.assertEqual(parts[1], "2")
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
