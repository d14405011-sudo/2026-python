def main():
    while True:
        n = int(input())

        if n == 0:
            break

        numbers = []
        for i in range(n):
            x = int(input())
            numbers.append(x)

        numbers.sort()

        if n % 2 == 1:
            idx = n // 2
            median = numbers[idx]

            min_count = numbers.count(median)

            opt_count = 1

            print(median, min_count, opt_count)
        else:
            lower_idx = n // 2 - 1
            upper_idx = n // 2

            lower = numbers[lower_idx]
            upper = numbers[upper_idx]

            min_count = numbers.count(lower)

            opt_count = upper - lower + 1

            print(lower, min_count, opt_count)

if __name__ == "__main__":
    main()
