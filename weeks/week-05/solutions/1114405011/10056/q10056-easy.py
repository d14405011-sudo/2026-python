"""Q10056 簡化版本 - 適合考試"""

def solve():
    s = int(input())
    for _ in range(s):
        n, p, i = map(float, input().split())
        n, i = int(n), int(i)
        
        # P_i = p * (1-p)^(i-1) / (1 - (1-p)^n)
        denom = 1 - ((1 - p) ** n)
        if denom == 0:
            prob = 0.0
        else:
            prob = (p * ((1 - p) ** (i - 1))) / denom
        print(f"{prob:.4f}")

solve()
