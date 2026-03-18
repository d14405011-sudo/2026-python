import sys


def solve(data):
    out = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break

        carry = 0
        cnt = 0
        while a > 0 or b > 0:
            s = (a % 10) + (b % 10) + carry
            if s >= 10:
                cnt += 1
                carry = 1
            else:
                carry = 0
            a //= 10
            b //= 10

        if cnt == 0:
            out.append("No carry operation.")
        elif cnt == 1:
            out.append("1 carry operation.")
        else:
            out.append(f"{cnt} carry operations.")

    return "\n".join(out) + ("\n" if out else "")


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
import sys

def solve(data):
    out = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break

        carry = 0
        cnt = 0
        while a > 0 or b > 0:
            s = (a % 10) + (b % 10) + carry
            if s >= 10:
                cnt += 1
                carry = 1
            else:
                carry = 0
            a //= 10
            b //= 10

        if cnt == 0:
            out.append("No carry operation.")
        elif cnt == 1:
            out.append("1 carry operation.")
        else:
            out.append(f"{cnt} carry operations.")

    return "\n".join(out) + ("\n" if out else "")

if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))