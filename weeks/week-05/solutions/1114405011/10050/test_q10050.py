"""
UVA 10050 - Hartals (罷工) 測試程式
題目：計算 N 天內因為政黨罷工損失的工作天數
"""

import unittest
from io import StringIO
import sys


def solve_q10050():
    """
    解決 UVA 10050 - Hartals
    模擬多個政黨的罷工情況，計算工作天損失
    """
    t = int(input())
    for _ in range(t):
        n = int(input())  # 模擬天數
        p = int(input())  # 政黨數
        
        # 記錄哪些天會罷工
        strike_days = set()
        
        # 處理每個政黨的罷工
        for _ in range(p):
            h = int(input())  # 該政黨的罷工參數
            
            # 每隔 h 天罷工一次
            day = h  # 第一次罷工在第 h 天
            while day <= n:
                # 檢查是否為工作日（不是周五或周六）
                day_of_week = ((day - 1) % 7) + 1  # 1=星期日, 2=星期一, ..., 7=星期六
                
                # 周五是第 6 天，周六是第 7 天
                if day_of_week not in [6, 7]:
                    strike_days.add(day)
                
                day += h
        
        # 輸出罷工天數
        print(len(strike_days))


class TestQ10050(unittest.TestCase):
    """Q10050 的單元測試"""
    
    def solve_with_input(self, input_str):
        """
        模擬輸入並執行程式
        """
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = StringIO(input_str)
        sys.stdout = StringIO()
        
        try:
            solve_q10050()
            output = sys.stdout.getvalue()
            return output.strip()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
    
    def test_simple_case(self):
        """測試範例：14天，3個政黨，h=3,4,8"""
        input_data = """1
14
3
3
4
8"""
        # 預期: 5天罷工（第3, 4, 8, 9, 12天）
        # 第6天是周五，第7天是周六，不計數
        expected = "5"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)
    
    def test_single_party(self):
        """測試單一政黨"""
        input_data = """1
10
1
2"""
        # h=2 的政黨在第 2, 4, 6, 8, 10 天
        # 但第 6 天和第 7 天不計
        # 實際: 2, 4, 8, 10 (第6天被排除)
        # 等等，需要驗算 weekday
        # 1=日, 2=一, 3=二, 4=三, 5=四, 6=五, 7=六
        # 第1天=日, 第2天=一, 第3天=二, 第4天=三, 第5天=四, 第6天=五, 第7天=六
        # 第8天=日, 第9天=一, 第10天=二
        # 所以 2, 4, 8, 10 都是工作日 = 4天
        expected = "4"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)
    
    def test_weekend_exclusion(self):
        """測試周末排除"""
        input_data = """1
14
1
7"""
        # h=7 的政黨在第 7, 14 天
        # 第 7 天是周六，第 14 天是周五（1+13=14, (13%7)+1=7，所以14是周日）
        # 重新計算：天 1=日, 2=一, ..., 7=六, 8=日, 9=一, ..., 14=日
        # 第 7 天是周六（不計），第 14 天是周日（計）
        # 等等，這個需要驗算
        # 第 7 天：(7-1)%7+1 = 6%7+1 = 7（周六，不計）
        # 第 14 天：(14-1)%7+1 = 13%7+1 = 7（周六，不計）
        # 所以結果應該是 0
        # 但讓我重新確認：h=7意味著7天罷工一次
        # 在14天內，罷工日期是第7天和第14天（都是周六），所以0天
        # 但題目說「假設在每週的假日(星期五和星期六)不會有任何罷工情形」
        # 這表示罷工不會在周五或周六發生
        # 所以我們應該跳過那些日期
        # 第 7, 14 都是周六，都不計，所以答案是 0
        # 但這樣的話可能會「跳過」周五和周六之後再罷工嗎？不，題目的意思是他們不罷工
        expected = "0"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)
    
    def test_multiple_parties(self):
        """測試多個政黨"""
        input_data = """1
7
2
2
3"""
        # h=2: 第 2, 4, 6（周五，不計）, 可能沒有6... 等等
        # (6-1)%7+1 = 5%7+1 = 6（周五），不計
        # 所以 h=2: 2, 4 兩天
        # h=3: 第 3, 6（周五，不計）, 沒了
        # 所以 h=3: 3 一天
        # 合併：2, 3, 4 三天
        expected = "3"
        result = self.solve_with_input(input_data)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
