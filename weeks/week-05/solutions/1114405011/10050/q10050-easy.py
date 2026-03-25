"""Q10050 簡化版本 - 適合考試"""

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = int(input())
        strikes = set()
        
        for _ in range(p):
            h = int(input())
            day = h
            while day <= n:
                # 計算星期幾（1=日...7=六）
                weekday = ((day - 1) % 7) + 1
                # 如果不是周五(6)或周六(7)，記錄罷工
                if weekday not in [6, 7]:
                    strikes.add(day)
                day += h
        
        print(len(strikes))

solve()
