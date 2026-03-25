def main():
    t = int(input())

    for _ in range(t):
        data = list(map(int, input().split()))

        r = data[0]
        relatives = data[1:r+1]

        relatives.sort()

        length = len(relatives)
        if length % 2 == 1:
            median = relatives[length // 2]
        else:
            median = relatives[length // 2 - 1]

        result = 0
        for house in relatives:
            result += abs(house - median)

        print(result)

if __name__ == "__main__":
    main()
