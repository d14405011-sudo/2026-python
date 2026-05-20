"""UVA 11332（本課版本：原點看鏡子可視性）
一般版：含繁體中文註解

說明：此解法使用「角度採樣」判定可見鏡子，
在本課常見測資可有效工作。
"""

from __future__ import annotations

import math

EPS = 1e-10
TAU = 2.0 * math.pi


class Segment:
    def __init__(self, sx: float, sy: float, ex: float, ey: float) -> None:
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey


def norm_ang(a: float) -> float:
    while a < 0:
        a += TAU
    while a >= TAU:
        a -= TAU
    return a


def cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def ray_hit_t(seg: Segment, ang: float) -> float | None:
    """回傳射線與線段交點的 t（原點 + t*dir），若無交點回傳 None。"""
    dx = math.cos(ang)
    dy = math.sin(ang)

    px, py = seg.sx, seg.sy
    vx, vy = seg.ex - seg.sx, seg.ey - seg.sy

    den = cross(dx, dy, vx, vy)

    if abs(den) < EPS:
        # 平行或共線情況：只處理共線且在線前方的部分。
        if abs(cross(px, py, dx, dy)) > EPS or abs(cross(seg.ex, seg.ey, dx, dy)) > EPS:
            return None

        t1 = px * dx + py * dy
        t2 = seg.ex * dx + seg.ey * dy
        cand = [t for t in (t1, t2) if t > EPS]
        return min(cand) if cand else None

    t = cross(px, py, vx, vy) / den
    u = cross(px, py, dx, dy) / den

    if t > EPS and -EPS <= u <= 1 + EPS:
        return t
    return None


def solve_one(n: int, segs: list[Segment]) -> str:
    if n == 0:
        return ""

    angs = []
    for s in segs:
        angs.append(norm_ang(math.atan2(s.sy, s.sx)))
        angs.append(norm_ang(math.atan2(s.ey, s.ex)))

    angs = sorted(set(angs))
    samples: list[float] = []

    # 取端點角度附近與相鄰角區間中點，減少落在邊界造成的不穩定。
    for a in angs:
        samples.append(norm_ang(a - 1e-7))
        samples.append(a)
        samples.append(norm_ang(a + 1e-7))

    for i in range(len(angs)):
        a = angs[i]
        b = angs[(i + 1) % len(angs)]
        if i == len(angs) - 1:
            b += TAU
        samples.append(norm_ang((a + b) / 2.0))

    visible = [0] * n

    for ang in samples:
        best_t = float("inf")
        best_i = -1
        for i, seg in enumerate(segs):
            t = ray_hit_t(seg, ang)
            if t is not None and t < best_t:
                best_t = t
                best_i = i
        if best_i >= 0:
            visible[best_i] = 1

    return " ".join(map(str, visible))


def solve(text: str) -> str:
    vals = list(map(int, text.split()))
    i = 0
    out: list[str] = []

    while i < len(vals):
        n = vals[i]
        i += 1
        if n <= 0:
            break

        segs: list[Segment] = []
        for _ in range(n):
            sx, sy, ex, ey = vals[i], vals[i + 1], vals[i + 2], vals[i + 3]
            i += 4
            segs.append(Segment(sx, sy, ex, ey))

        out.append(solve_one(n, segs))

    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
