"""
UVA 10050 - Hartals (罷工)
題目：計算 N 天內因為多個政黨罷工損失的工作天數

解題思路：
========
1. 每個政黨每隔 h 天罷工一次
2. 周五（weekday=6）和周六（weekday=7）不會罷工
3. 用集合記錄罷工天數，自動去重複
4. 計算集合的大小

日期轉換：
========
- 星期日=1, 星期一=2, ..., 星期六=7
- 第 n 天的星期幾：((n-1) % 7) + 1
"""

def solve_q10050():
    """
    主程式：計算罷工導致的工作天損失
    """
    t = int(input())  # 測試資料組數
    for _ in range(t):
        n = int(input())  # 模擬的天數
        p = int(input())  # 政黨數
        
        # 用集合記錄罷工的工作天
        strike_days = set()
        
        # 處理每個政黨
        for _ in range(p):
            h = int(input())  # 這個政黨的罷工參數
            
            # 該政黨每隔 h 天罷工一次
            day = h  # 第一次罷工在第 h 天
            while day <= n:
                # 計算這一天是周幾（1=日, 2=一, ..., 7=六）
                day_of_week = ((day - 1) % 7) + 1
                
                # 只有在工作日（不是周五或周六）才記錄罷工
                if day_of_week not in [6, 7]:
                    strike_days.add(day)
                
                # 下次罷工
                day += h
        
        # 輸出罷工天數
        print(len(strike_days))


if __name__ == "__main__":
    solve_q10050()
