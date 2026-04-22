"""
題號 10226 一般版解法

重點整理：
1) 有 N 個人（A, B, C...），每人有不想站的位置清單。
2) 需輸出所有合法排列，並以字典序排列。
3) 與前一次輸出相同的前綴不重複輸出，只輸出不同後綴。

此版本使用回溯法依位置遞迴，直接保證字典序。
"""

from __future__ import annotations

from typing import Iterable, List, Set, Tuple


def parse_cases(raw: str) -> List[Tuple[int, List[Set[int]]]]:
    """解析輸入，支援以下兩種格式：
    1) 第一行為 T，接著 T 組測資。
    2) 直接多組測資到 EOF。

    每組測資格式：
    - 一行 N
    - 接著 N 行，每行為該人不想站的位置，0 結束
    """
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        return []

    def parse_from(start: int, total_cases: int | None) -> Tuple[List[Tuple[int, List[Set[int]]]], int] | None:
        idx = start
        cases: List[Tuple[int, List[Set[int]]]] = []

        while idx < len(lines) and (total_cases is None or len(cases) < total_cases):
            try:
                n = int(lines[idx])
            except ValueError:
                return None
            idx += 1
            if n < 1:
                return None
            if idx + n > len(lines):
                return None

            banned: List[Set[int]] = []
            for _ in range(n):
                try:
                    nums = [int(x) for x in lines[idx].split()]
                except ValueError:
                    return None
                idx += 1
                s: Set[int] = set()
                for v in nums:
                    if v == 0:
                        break
                    s.add(v)
                banned.append(s)
            cases.append((n, banned))

        if total_cases is not None and len(cases) != total_cases:
            return None
        return cases, idx

    # 先嘗試第一行是 T
    try:
        t = int(lines[0])
    except ValueError:
        t = -1

    if t >= 1:
        parsed = parse_from(1, t)
        if parsed is not None:
            cases, end_idx = parsed
            if end_idx == len(lines):
                return cases

    # 若不符合，就改成直接讀到 EOF
    parsed = parse_from(0, None)
    if parsed is None:
        return []
    cases, _ = parsed
    return cases


def generate_arrangements(n: int, banned: List[Set[int]]) -> List[str]:
    """生成所有合法排列字串（位置視角），並保證字典序。"""
    people = [chr(ord("A") + i) for i in range(n)]
    used = [False] * n
    placed: List[str] = [""] * n
    ans: List[str] = []

    def backtrack(pos: int) -> None:
        # pos 為 1-based 位置編號（方便對照題目位置描述）
        if pos > n:
            ans.append("".join(placed))
            return

        # 依字母順序嘗試，完成後即是字典序輸出
        for person_idx, person in enumerate(people):
            if used[person_idx]:
                continue
            if pos in banned[person_idx]:
                continue
            used[person_idx] = True
            placed[pos - 1] = person
            backtrack(pos + 1)
            used[person_idx] = False

    backtrack(1)
    return ans


def compress_by_lcp(arrangements: Iterable[str]) -> List[str]:
    """依題意壓縮輸出：與前一筆相同前綴不重複印出，只保留差異後綴。"""
    out: List[str] = []
    prev = ""
    first = True
    for cur in arrangements:
        if first:
            out.append(cur)
            prev = cur
            first = False
            continue

        lcp = 0
        for a, b in zip(prev, cur):
            if a != b:
                break
            lcp += 1
        out.append(cur[lcp:])
        prev = cur
    return out


def solve(raw: str) -> str:
    cases = parse_cases(raw)
    outputs: List[str] = []

    for i, (n, banned) in enumerate(cases):
        arrangements = generate_arrangements(n, banned)
        compressed = compress_by_lcp(arrangements)
        outputs.extend(compressed)
        if i != len(cases) - 1:
            outputs.append("")

    return "\n".join(outputs)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print(solve(data), end="")
