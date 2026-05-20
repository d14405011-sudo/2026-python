"""UVA 11332（本課版本：原點看鏡子可視性）
簡單好記版：含繁體中文詳細註解
"""

from __future__ import annotations

import math

EPS = 1e-10
TAU = 2.0 * math.pi


def c(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def na(a: float) -> float:
    while a < 0:
        a += TAU
    while a >= TAU:
        a -= TAU
    return a


def hit(seg: tuple[float, float, float, float], ang: float) -> float | None:
    sx, sy, ex, ey = seg
    dx, dy = math.cos(ang), math.sin(ang)
    vx, vy = ex - sx, ey - sy
    den = c(dx, dy, vx, vy)

    if abs(den) < EPS:
        if abs(c(sx, sy, dx, dy)) > EPS or abs(c(ex, ey, dx, dy)) > EPS:
            return None
        t1 = sx * dx + sy * dy
        t2 = ex * dx + ey * dy
        cand = [x for x in (t1, t2) if x > EPS]
        return min(cand) if cand else None

    t = c(sx, sy, vx, vy) / den
    u = c(sx, sy, dx, dy) / den
    if t > EPS and -EPS <= u <= 1 + EPS:
        return t
    return None


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    p = 0
    out: list[str] = []

    while p < len(a):
        n = a[p]
        p += 1
        if n <= 0:
            break

        segs = []
        angs = []
        for _ in range(n):
            sx, sy, ex, ey = a[p], a[p + 1], a[p + 2], a[p + 3]
            p += 4
            segs.append((sx, sy, ex, ey))
            angs.append(na(math.atan2(sy, sx)))
            angs.append(na(math.atan2(ey, ex)))

        angs = sorted(set(angs))
        smp = []
        for x in angs:
            smp.extend([na(x - 1e-7), x, na(x + 1e-7)])
        for i in range(len(angs)):
            l = angs[i]
            r = angs[(i + 1) % len(angs)]
            if i == len(angs) - 1:
                r += TAU
            smp.append(na((l + r) / 2.0))

        vis = [0] * n
        for ang in smp:
            best = float("inf")
            idx = -1
            for i, seg in enumerate(segs):
                t = hit(seg, ang)
                if t is not None and t < best:
                    best = t
                    idx = i
            if idx >= 0:
                vis[idx] = 1

        out.append(" ".join(map(str, vis)))

    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
