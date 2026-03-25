def main():
    while True:
        # Read number of elements; stop cleanly at EOF
        try:
            line = input()
        except EOFError:
            break

        if not line:
            # Skip empty lines, if any
            continue

        n = int(line)

        numbers = []
        for i in range(n):
            try:
                x = int(input())
            except EOFError:
                # Unexpected EOF in the middle of a test case; stop processing
                return
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
