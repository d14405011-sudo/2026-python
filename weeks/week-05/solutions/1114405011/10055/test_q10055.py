"""
UVA 10055 - 複合函數的增減性 測試程式
題目：判斷複合函數的增減性
"""

import unittest
from io import StringIO
import sys


def solve_q10055():
    """
    解決 UVA 10055 - 複合函數增減性
    """
    n, q = map(int, input().split())
    
    # 0 = 增函數, 1 = 減函數
    # 一開始所有函數都是增函數
    functions = [0] * (n + 1)  # 1-indexed
    
    for _ in range(q):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            # 翻轉操作
            i = query[1]
            functions[i] = 1 - functions[i]  # 0->1, 1->0
        else:
            # 查詢操作
            l = query[1]
            r = query[2]
            
            # 計算複合函數的增減性
            # 規則：偶數個減函數 = 增(0), 奇數個減函數 = 減(1)
            count_decreasing = sum(functions[l:r+1])
            result = count_decreasing % 2
            
            print(result)


class TestQ10055(unittest.TestCase):
    """Q10055 的單元測試"""
    
    def solve_with_input(self, input_str):
        """
        模擬輸入並執行程式
        """
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = StringIO(input_str)
        sys.stdout = StringIO()
        
        try:
            solve_q10055()
            output = sys.stdout.getvalue()
            return output.strip()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
    
    def test_simple_query(self):
        """測試簡單查詢"""
        input_data = """3 2
2 1 3
2 1 2"""
        # 所有函數一開始都是增(0)
        # 查詢1: f1, f2, f3 都是增 -> 複合 = 增 -> 輸出 0
        # 查詢2: f1, f2 都是增 -> 複合 = 增 -> 輸出 0
        result_lines = self.solve_with_input(input_data).split('\n')
        self.assertEqual(result_lines[0], "0")
        self.assertEqual(result_lines[1], "0")
    
    def test_flip_operation(self):
        """測試翻轉操作"""
        input_data = """2 3
1 1
2 1 2
2 1 1"""
        # 翻轉 f1: f1=1(減), f2=0(增)
        # 查詢1: f1, f2 -> 1個減 -> 奇數 -> 輸出 1
        # 查詢2: f1 -> 1個減 -> 奇數 -> 輸出 1
        result_lines = self.solve_with_input(input_data).split('\n')
        self.assertEqual(result_lines[0], "1")
        self.assertEqual(result_lines[1], "1")
    
    def test_multiple_flips(self):
        """測試多次翻轉"""
        input_data = """2 5
1 1
1 1
2 1 2
1 2
2 1 2"""
        # 翻轉 f1: f1=1
        # 翻轉 f1 再一次: f1=0
        # 查詢: f1, f2 都是增 -> 輸出 0
        # 翻轉 f2: f2=1
        # 查詢: f1=0, f2=1 -> 1個減 -> 輸出 1
        result_lines = self.solve_with_input(input_data).split('\n')
        self.assertEqual(result_lines[0], "0")
        self.assertEqual(result_lines[1], "1")
    
    def test_even_decreasing(self):
        """測試偶數個減函數"""
        input_data = """3 4
1 1
1 2
2 1 3
2 2 3"""
        # 翻轉 f1: f1=1(減)
        # 翻轉 f2: f2=1(減)
        # 查詢: f1,f2,f3 -> 2個減(偶數) -> 增 -> 輸出 0
        # 查詢: f2,f3 -> 1個減(奇數) -> 減 -> 輸出 1
        result_lines = self.solve_with_input(input_data).split('\n')
        self.assertEqual(result_lines[0], "0")
        self.assertEqual(result_lines[1], "1")


if __name__ == '__main__':
    unittest.main()
