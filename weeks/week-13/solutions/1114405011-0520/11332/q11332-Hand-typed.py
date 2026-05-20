from __future__ import annotations

import math

EPS = 1e-10
TAU = 2.0 * math.pi


def cr(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def nm(a: float) -> float:
    while a < 0:
        a += TAU
    while a >= TAU:
        a -= TAU
    return a


def hit(seg: tuple[float, float, float, float], ang: float) -> float | None:
    sx, sy, ex, ey = seg
    dx, dy = math.cos(ang), math.sin(ang)
    vx, vy = ex - sx, ey - sy
    den = cr(dx, dy, vx, vy)

    if abs(den) < EPS:
        if abs(cr(sx, sy, dx, dy)) > EPS or abs(cr(ex, ey, dx, dy)) > EPS:
            return None
        t1 = sx * dx + sy * dy
        t2 = ex * dx + ey * dy
        c = [t for t in (t1, t2) if t > EPS]
        return min(c) if c else None

    t = cr(sx, sy, vx, vy) / den
    u = cr(sx, sy, dx, dy) / den
    if t > EPS and -EPS <= u <= 1 + EPS:
        return t
    return None


def solve(text: str) -> str:
    a = list(map(int, text.split()))
    i = 0
    out: list[str] = []

    while i < len(a):
        n = a[i]
        i += 1
        if n <= 0:
            break

        segs = []
        ang = []
        for _ in range(n):
            sx, sy, ex, ey = a[i], a[i + 1], a[i + 2], a[i + 3]
            i += 4
            segs.append((sx, sy, ex, ey))
            ang.append(nm(math.atan2(sy, sx)))
            ang.append(nm(math.atan2(ey, ex)))

        ang = sorted(set(ang))
        sm = []
        for x in ang:
            sm.extend([nm(x - 1e-7), x, nm(x + 1e-7)])
        for k in range(len(ang)):
            l = ang[k]
            r = ang[(k + 1) % len(ang)]
            if k == len(ang) - 1:
                r += TAU
            sm.append(nm((l + r) / 2.0))

        vis = [0] * n
        for a0 in sm:
            best = float("inf")
            who = -1
            for j, seg in enumerate(segs):
                t = hit(seg, a0)
                if t is not None and t < best:
                    best = t
                    who = j
            if who >= 0:
                vis[who] = 1

        out.append(" ".join(map(str, vis)))

    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
