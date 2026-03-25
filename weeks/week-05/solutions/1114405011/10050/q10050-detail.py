"""
UVA 10050 - Hartals (詳細版本)

問題詳解：
========
Vito 所在國的政黨會定期罷工。每個政黨有一個罷工參數 h，表示連續兩次罷工的間隔天數。

規則：
1. 第 i 個政黨在第 h, 2h, 3h, ... 天罷工
2. 周五和周六是假日，不發生罷工
3. 計算 N 天內因罷工損失的工作天數

日期計算公式：
第 n 天的星期幾 = ((n - 1) % 7) + 1
- 1 = 星期日（Sunday）
- 2 = 星期一（Monday）
- 3 = 星期二（Tuesday）
- 4 = 星期三（Wednesday）
- 5 = 星期四（Thursday）
- 6 = 星期五（Friday） ← 假日
- 7 = 星期六（Saturday） ← 假日

演算法：
1. 對每個政黨，計算其罷工的所有工作日
2. 使用集合去除重複（多個政黨可能在同一天罷工）
3. 輸出集合大小

時間複雜度：O(P * (N / h))，其中 P 是政黨數
空間複雜度：O(N)
"""

import sys

def solve_q10050_detailed():
    """
    詳細版本的 Q10050 解決方案
    """
    t = int(input())
    
    for test_case in range(1, t + 1):
        n = int(input())  # 模擬天數
        p = int(input())  # 政黨數
        
        print(f"[測試 #{test_case}]", file=sys.stderr)
        print(f"  模擬天數: {n}", file=sys.stderr)
        print(f"  政黨數: {p}", file=sys.stderr)
        
        strikes = set()
        
        for party_idx in range(1, p + 1):
            h = int(input())  # 這個政黨的罷工參數
            party_strikes = []
            
            day = h
            while day <= n:
                weekday = ((day - 1) % 7) + 1
                weekday_name = ['', '日', '一', '二', '三', '四', '五', '六'][weekday]
                
                if weekday not in [6, 7]:
                    strikes.add(day)
                    party_strikes.append(day)
                
                day += h
            
            print(f"  政黨 {party_idx} (h={h}): 罷工日期 = {party_strikes}", file=sys.stderr)
        
        print(f"  全部罷工日期（去重）: {sorted(strikes)}", file=sys.stderr)
        print(f"  總罷工天數: {len(strikes)}", file=sys.stderr)
        
        print(len(strikes))


if __name__ == "__main__":
    solve_q10050_detailed()
