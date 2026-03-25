"""
UVA 10041 - Vito's Family 測試程式
題目：找到距離所有親戚房子總距離最小的位置（中位數問題）
"""

import unittest
from io import StringIO
import sys

# Q10041 解決方案
def solve_q10041():
    """
    解決 UVA 10041 - Vito's Family
    使用中位數找到最小距離和
    """
    t = int(input())
    for _ in range(t):
        line = list(map(int, input().split()))
        r = line[0]
        relatives = line[1:r+1]
        
        # 對親戚的房子門牌號碼排序
        relatives.sort()
        
        # 取中位數作為最優位置
        if len(relatives) % 2 == 1:
            # 奇數個親戚，取中間位置
            median = relatives[len(relatives) // 2]
        else:
            # 偶數個親戚，取中間兩個的任意一個都可以
            median = relatives[len(relatives) // 2 - 1]
        
        # 計算距離和
        total_distance = sum(abs(house - median) for house in relatives)
        print(total_distance)


class TestQ10041(unittest.TestCase):
    """Q10041 的單元測試"""
    
    def solve_with_input(self, input_str):
        """
        模擬輸入並執行程式
        """
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = StringIO(input_str)
        sys.stdout = StringIO()
        
        try:
            solve_q10041()
            output = sys.stdout.getvalue()
            return output.strip()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
    
    def test_simple_case(self):
        """測試簡單案例：3個親戚"""
        input_data = """1
3 2 4 6"""
        expected = "4"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)
    
    def test_single_relative(self):
        """測試單一親戚"""
        input_data = """1
1 10"""
        expected = "0"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)
    
    def test_multiple_testcases(self):
        """測試多個測試資料"""
        input_data = """2
3 2 4 6
4 1 3 5 7"""
        result_lines = self.solve_with_input(input_data).split('\n')
        # 第一組測資：中位數是4，距離=(2-4)+(4-4)+(6-4)=4
        self.assertEqual(result_lines[0], "4")
        # 第二組測資：4個親戚，下中位數是3: (1-3)+(3-3)+(5-3)+(7-3)=2+0+2+4=8
        self.assertEqual(result_lines[1], "8")
    
    def test_even_relatives(self):
        """測試偶數個親戚"""
        input_data = """1
4 1 2 8 9"""
        # 中位數在 1 到 9 之間，選 2 或 8 都可以
        # 選 2: |1-2|+|2-2|+|8-2|+|9-2| = 1+0+6+7 = 14
        expected = "14"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)
    
    def test_duplicate_relatives(self):
        """測試有重複門牌號碼的情況"""
        input_data = """1
5 5 5 5 5 5"""
        # 所有親戚在同一位置，距離和為 0
        expected = "0"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)
    
    def test_large_numbers(self):
        """測試大數字"""
        input_data = """1
3 10000 20000 30000"""
        # 中位數是 20000，距離=(10000)+(0)+(10000)=20000
        expected = "20000"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
