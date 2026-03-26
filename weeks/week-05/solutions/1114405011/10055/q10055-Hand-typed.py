def main():
    line = input().split()
    n = int(line[0])
    q = int(line[1])

    # functions[i] stores the current value (0 or 1) at position i
    functions = [0] * (n + 1)

    # Fenwick Tree (Binary Indexed Tree) for prefix sums over functions[1..n]
    bit = [0] * (n + 1)

    def update(i, delta):
        """Add delta to position i in the Fenwick Tree."""
        while i <= n:
            bit[i] += delta
            i += i & -i

    def query(i):
        """Return the prefix sum from 1 to i."""
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    for _ in range(q):
        query_line = input().split()
        query_type = int(query_line[0])

        if query_type == 1:
            i = int(query_line[1])
            # Toggle functions[i] and update Fenwick Tree accordingly
            delta = 1 - 2 * functions[i]  # +1 if 0->1, -1 if 1->0
            functions[i] = 1 - functions[i]
            update(i, delta)
        else:
            l = int(query_line[1])
            r = int(query_line[2])

            # Count how many j in [l, r] have functions[j] == 1
            decreasing_count = query(r) - query(l - 1)

            if decreasing_count % 2 == 0:
                result = 0
            else:
                result = 1

            print(result)

if __name__ == "__main__":
    main()
