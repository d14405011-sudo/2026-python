"""Q10055 簡化版本 - 適合考試"""

def solve():
    n, q = map(int, input().split())
    funcs = [0] * (n + 1)  # 0=增, 1=減
    
    for _ in range(q):
        op = list(map(int, input().split()))
        if op[0] == 1:
            # 翻轉操作
            funcs[op[1]] = 1 - funcs[op[1]]
        else:
            # 查詢操作：計算減函數個數的奇偶性
            decreasing_count = sum(funcs[op[1]:op[2]+1])
            print(decreasing_count % 2)

solve()
