def main():
    t = int(input())

    for _ in range(t):
        n = int(input())

        p = int(input())

        strike_days = set()

        for i in range(p):
            h = int(input())

            day = h
            while day <= n:
                weekday = ((day - 1) % 7) + 1

                if weekday != 6 and weekday != 7:
                    strike_days.add(day)

                day = day + h

        print(len(strike_days))

if __name__ == "__main__":
    main()
