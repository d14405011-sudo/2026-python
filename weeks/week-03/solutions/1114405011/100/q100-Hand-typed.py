import sys


def cycle_length(n):
    count = 1
    while n != 1:
        if n % 2 == 1:
            n = 3 * n + 1
        else:
            n = n // 2
        count += 1
    return count

def max_cycle_in_range(i, j):
    lo, hi = min(i, j), max(i, j)
    best = 0
    for n in range(lo, hi + 1):
        cl = cycle_length(n)
        if cl > best:
            best = cl
    return best

def solve(input_text):
    output_lines = []
    for line in input_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        i, j = map(int, line.split())
        output_lines.append(f"{i} {j} {max_cycle_in_range(i, j)}")
    return "\n".join(output_lines)


def read_input_text():
    """
    支援兩種模式：
    1) judge/重導輸入：直接讀 sys.stdin
    2) 互動執行：逐行輸入，空白行結束
    """
    if not sys.stdin.isatty():
        return sys.stdin.read()

    print("請輸入多行 'i j'，輸入空白行結束：", file=sys.stderr)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    input_text = read_input_text()
    if input_text.strip():
        print(solve(input_text))
    else:
        print("未提供有效輸入。", file=sys.stderr)