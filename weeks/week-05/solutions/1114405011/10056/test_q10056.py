"""
UVA 10056 - Dice (骰子機率) 測試程式
題目：計算指定玩家的獲勝機率
"""

import unittest
from io import StringIO
import sys


def solve_q10056():
    """
    解決 UVA 10056 - 骰子機率
    """
    s = int(input())
    
    for _ in range(s):
        n, p, i = map(float, input().split())
        n = int(n)
        i = int(i)
        
        # 計算第 i 個玩家的獲勝機率
        # 公式：P_i = p * (1-p)^(i-1) / (1 - (1-p)^n)
        
        prob = (p * ((1 - p) ** (i - 1))) / (1 - ((1 - p) ** n))
        
        # 輸出四位小數
        print(f"{prob:.4f}")


class TestQ10056(unittest.TestCase):
    """Q10056 的單元測試"""
    
    def solve_with_input(self, input_str):
        """
        模擬輸入並執行程式
        """
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = StringIO(input_str)
        sys.stdout = StringIO()
        
        try:
            solve_q10056()
            output = sys.stdout.getvalue()
            return output.strip()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
    
    def test_single_player(self):
        """測試單一玩家"""
        input_data = """1
1 0.5 1"""
        # n=1, p=0.5, i=1
        # 機率：0.5 * (0.5)^0 / (1 - 0.5) = 0.5 / 0.5 = 1.0
        result = self.solve_with_input(input_data)
        self.assertEqual(result, "1.0000")
    
    def test_two_players_equal(self):
        """測試兩個玩家，機率相等"""
        input_data = """1
2 0.5 1"""
        # n=2, p=0.5, i=1
        # 機率：0.5 * (0.5)^0 / (1 - (0.5)^2) = 0.5 / 0.75 = 2/3 ≈ 0.6667
        result = self.solve_with_input(input_data)
        self.assertAlmostEqual(float(result), 2/3, places=4)
    
    def test_two_players_second(self):
        """測試兩個玩家，查詢第二個玩家"""
        input_data = """1
2 0.5 2"""
        # n=2, p=0.5, i=2
        # 機率：0.5 * (0.5)^1 / (1 - 0.25) = 0.25 / 0.75 = 1/3 ≈ 0.3333
        result = self.solve_with_input(input_data)
        self.assertAlmostEqual(float(result), 1/3, places=4)
    
    def test_dice_example(self):
        """測試正常骰子，獲得 3 的機率"""
        input_data = """1
6 0.16667 3"""
        # 6 個玩家，p≈1/6，查詢第 3 個
        result = self.solve_with_input(input_data)
        # 應該是一個有效的機率值
        prob = float(result)
        self.assertGreater(prob, 0)
        self.assertLess(prob, 1)


if __name__ == '__main__':
    unittest.main()
