def main():
    s = int(input())

    for _ in range(s):
        line = input().split()
        n = int(line[0])
        p = float(line[1])
        i = int(line[2])

        q = 1.0 - p

        numerator = p * (q ** (i - 1))

        denominator = 1.0 - (q ** n)

        probability = numerator / denominator

        print(f"{probability:.4f}")

if __name__ == "__main__":
    main()
