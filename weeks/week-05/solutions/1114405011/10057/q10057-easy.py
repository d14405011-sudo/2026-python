"""Q10057 簡化版本 - 適合考試"""

def solve():
    while True:
        n = int(input())
        if n == 0:
            break
        
        nums = [int(input()) for _ in range(n)]
        nums.sort()
        
        if n % 2 == 1:
            # 奇數個
            mid = nums[n // 2]
            min_count = nums.count(mid)
            print(mid, min_count, 1)
        else:
            # 偶數個
            lower = nums[n // 2 - 1]
            upper = nums[n // 2]
            count = upper - lower + 1
            min_count = nums.count(lower)
            print(lower, min_count, count)

solve()
