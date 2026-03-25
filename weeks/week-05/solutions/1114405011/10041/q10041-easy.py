"""Q10041 簡化版本 - 適合考試"""

def solve():
    t = int(input())
    for _ in range(t):
        data = list(map(int, input().split()))
        r = data[0]
        houses = sorted(data[1:r+1])
        
        # 用中位數計算最小距離和
        mid = houses[len(houses) // 2 - 1] if len(houses) % 2 == 0 else houses[len(houses) // 2]
        total = sum(abs(h - mid) for h in houses)
        print(total)

solve()
