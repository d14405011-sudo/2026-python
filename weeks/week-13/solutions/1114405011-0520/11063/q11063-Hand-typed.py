from __future__ import annotations


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    if not a:
        return ""

    n = a[0]
    i = 1
    out: list[str] = []
    sy = 0.0

    for _ in range(n * n):
        r, g, b = a[i], a[i + 1], a[i + 2]
        i += 3
        x = 0.5149 * r + 0.3244 * g + 0.1607 * b
        y = 0.2654 * r + 0.6704 * g + 0.0642 * b
        z = 0.0248 * r + 0.1248 * g + 0.8504 * b
        sy += y
        out.append(f"{x:.4f} {y:.4f} {z:.4f}")

    out.append(f"The average of Y is {sy / (n * n):.4f}")
    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
