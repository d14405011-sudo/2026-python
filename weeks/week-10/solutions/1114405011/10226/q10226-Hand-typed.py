from __future__ import annotations

from typing import List, Set, Tuple


def parse_input(raw: str) -> List[Tuple[int, List[Set[int]]]]:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        return []

    def parse_cases(start: int, t: int | None):
        i = start
        out = []
        while i < len(lines) and (t is None or len(out) < t):
            n = int(lines[i])
            i += 1
            banned = []
            for _ in range(n):
                arr = list(map(int, lines[i].split()))
                i += 1
                s = set()
                for v in arr:
                    if v == 0:
                        break
                    s.add(v)
                banned.append(s)
            out.append((n, banned))
        if t is not None and len(out) != t:
            return None
        return out, i

    try:
        t = int(lines[0])
        got = parse_cases(1, t)
        if got is not None and got[1] == len(lines):
            return got[0]
    except Exception:
        pass

    got = parse_cases(0, None)
    return got[0] if got else []


def all_orders(n: int, banned: List[Set[int]]) -> List[str]:
    people = [chr(ord("A") + i) for i in range(n)]
    used = [False] * n
    cur = [""] * n
    ans: List[str] = []

    def dfs(pos: int) -> None:
        if pos == n:
            ans.append("".join(cur))
            return
        p = pos + 1
        for i in range(n):
            if used[i] or p in banned[i]:
                continue
            used[i] = True
            cur[pos] = people[i]
            dfs(pos + 1)
            used[i] = False

    dfs(0)
    return ans


def compress(lines: List[str]) -> List[str]:
    if not lines:
        return []
    out = [lines[0]]
    for i in range(1, len(lines)):
        a = lines[i - 1]
        b = lines[i]
        p = 0
        while p < len(a) and p < len(b) and a[p] == b[p]:
            p += 1
        out.append(b[p:])
    return out


def solve(raw: str) -> str:
    cases = parse_input(raw)
    out = []
    for i, (n, banned) in enumerate(cases):
        out.extend(compress(all_orders(n, banned)))
        if i != len(cases) - 1:
            out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()), end="")
