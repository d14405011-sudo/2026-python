test_cases = int(input())

for _ in range(test_cases):
    data = list(map(int, input().split()))
    num_relatives = data[0]
    positions = data[1:num_relatives + 1]
    positions.sort()
    median = positions[(len(positions) - 1) // 2]
    total_distance = sum(abs(pos - median) for pos in positions)
    print(total_distance)