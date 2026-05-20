"""UVA 11063（本課版本：RGB 轉 XYZ）
簡單好記版：含繁體中文詳細註解
"""

from __future__ import annotations


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    if not a:
        return ""

    n = a[0]
    p = 1

    ans: list[str] = []
    sum_y = 0.0

    # 一共 n*n 個像素，每個像素有 3 個整數（R, G, B）。
    for _ in range(n * n):
        r, g, b = a[p], a[p + 1], a[p + 2]
        p += 3

        x = 0.5149 * r + 0.3244 * g + 0.1607 * b
        y = 0.2654 * r + 0.6704 * g + 0.0642 * b
        z = 0.0248 * r + 0.1248 * g + 0.8504 * b

        sum_y += y
        ans.append(f"{x:.4f} {y:.4f} {z:.4f}")

    ans.append(f"The average of Y is {sum_y / (n * n):.4f}")
    return "\n".join(ans)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
