"""
UVA 10221 - Satellites

已知：
- 地球半徑 6440。
- 衛星高度 s，故半徑 r = 6440 + s。
- 角度可用 deg 或 min（1 deg = 60 min）。

要求：
- 弧長 arc = r * theta。
- 弦長 chord = 2 * r * sin(theta / 2)。
- 角度取較小夾角（若 > 180，改成 360 - angle）。
"""

import math


def compute_distances(s: float, a: float, unit: str) -> tuple[float, float]:
    """回傳 (arc_length, chord_length)。"""
    if unit == "min":
        a /= 60.0

    if a > 180.0:
        a = 360.0 - a

    r = 6440.0 + s
    rad = math.radians(a)

    arc = r * rad
    chord = 2.0 * r * math.sin(rad / 2.0)
    return arc, chord


def solve_line(s: float, a: float, unit: str) -> str:
    arc, chord = compute_distances(s, a, unit)
    return f"{arc:.6f} {chord:.6f}"


def solve_all(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        s_str, a_str, unit = line.split()
        out.append(solve_line(float(s_str), float(a_str), unit))
    return "\n".join(out)


def main() -> None:
    import sys

    data = sys.stdin.read()
    ans = solve_all(data)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
