"""UVA 11063（本課版本：RGB 轉 XYZ）
一般版：含繁體中文註解
"""

from __future__ import annotations


def to_xyz(r: int, g: int, b: int) -> tuple[float, float, float]:
    x = 0.5149 * r + 0.3244 * g + 0.1607 * b
    y = 0.2654 * r + 0.6704 * g + 0.0642 * b
    z = 0.0248 * r + 0.1248 * g + 0.8504 * b
    return x, y, z


def solve(text: str) -> str:
    vals = list(map(int, text.split()))
    if not vals:
        return ""

    i = 0
    n = vals[i]
    i += 1

    out: list[str] = []
    total_y = 0.0
    count = n * n

    for _ in range(count):
        r = vals[i]
        g = vals[i + 1]
        b = vals[i + 2]
        i += 3

        x, y, z = to_xyz(r, g, b)
        total_y += y
        out.append(f"{x:.4f} {y:.4f} {z:.4f}")

    avg_y = total_y / count if count else 0.0
    out.append(f"The average of Y is {avg_y:.4f}")
    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
