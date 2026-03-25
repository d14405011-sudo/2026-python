def main():
    line = input().split()
    n = int(line[0])
    q = int(line[1])

    functions = [0] * (n + 1)

    for _ in range(q):
        query = input().split()
        query_type = int(query[0])

        if query_type == 1:
            i = int(query[1])

            functions[i] = 1 - functions[i]
        else:
            l = int(query[1])
            r = int(query[2])

            decreasing_count = 0
            for j in range(l, r + 1):
                if functions[j] == 1:
                    decreasing_count = decreasing_count + 1

            if decreasing_count % 2 == 0:
                result = 0
            else:
                result = 1

            print(result)

if __name__ == "__main__":
    main()
