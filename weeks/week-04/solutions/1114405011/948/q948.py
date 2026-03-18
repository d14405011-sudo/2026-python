"""UVA/ZeroJudge 假幣問題（題號 948）解題程式。

此檔案提供：
1. 可重用的核心函式 `detect_fake_coin`。
2. 以字串為輸入、字串為輸出的 `solve`。
3. 命令列執行入口（讀 stdin、寫 stdout）。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence
import sys


@dataclass(frozen=True)
class Weighing:
    """儲存一次秤重資料。

    屬性：
    - left: 左盤硬幣編號列表
    - right: 右盤硬幣編號列表
    - result: 秤重結果，僅可能是 '<'、'>'、'='
    """

    left: Sequence[int]
    right: Sequence[int]
    result: str


def _is_consistent(coin: int, state: str, weighings: Sequence[Weighing]) -> bool:
    """檢查「coin 是假幣且 state（heavy/light）」是否符合所有秤重結果。

    觀念：
    - 真幣重量都相同，且題目保證每次左右放的硬幣數相同。
    - 因此只要比較「假幣造成的淨影響」即可，不需要真的設定絕對重量。
    - `diff = 左盤影響 - 右盤影響`
      * diff < 0 代表左邊較輕（對應 '<'）
      * diff > 0 代表左邊較重（對應 '>'）
      * diff == 0 代表平衡（對應 '='）
    """

    for w in weighings:
        left_has_coin = coin in w.left
        right_has_coin = coin in w.right

        # 假幣若偏重，出現在某一邊會讓該邊 +1；偏輕則 -1。
        if state == "heavy":
            left_effect = 1 if left_has_coin else 0
            right_effect = 1 if right_has_coin else 0
        else:  # state == "light"
            left_effect = -1 if left_has_coin else 0
            right_effect = -1 if right_has_coin else 0

        diff = left_effect - right_effect

        if w.result == "=" and diff != 0:
            return False
        if w.result == "<" and not (diff < 0):
            return False
        if w.result == ">" and not (diff > 0):
            return False

    return True


def detect_fake_coin(n: int, weighings: Sequence[Weighing]) -> int:
    """回傳唯一可判定的假幣編號；若無法唯一判定，回傳 0。"""

    candidates: List[int] = []

    for coin in range(1, n + 1):
        # 只要「偏重」或「偏輕」其中一種狀態成立，此硬幣就仍是候選。
        can_be_heavy = _is_consistent(coin, "heavy", weighings)
        can_be_light = _is_consistent(coin, "light", weighings)

        if can_be_heavy or can_be_light:
            candidates.append(coin)

    return candidates[0] if len(candidates) == 1 else 0


def solve(raw: str) -> str:
    """將整份輸入字串轉成輸出字串。

    這題的輸入包含空白行；採用 token 解析可自然忽略空白行，
    且對 UVA/ZeroJudge 常見格式都很穩定。
    """

    tokens = raw.split()
    if not tokens:
        return ""

    idx = 0
    m = int(tokens[idx])
    idx += 1

    outputs: List[str] = []

    for _ in range(m):
        n = int(tokens[idx])
        k = int(tokens[idx + 1])
        idx += 2

        weighings: List[Weighing] = []
        for _ in range(k):
            p = int(tokens[idx])
            idx += 1

            left = [int(tokens[idx + i]) for i in range(p)]
            idx += p
            right = [int(tokens[idx + i]) for i in range(p)]
            idx += p

            result = tokens[idx]
            idx += 1

            weighings.append(Weighing(left=left, right=right, result=result))

        outputs.append(str(detect_fake_coin(n, weighings)))

    # 題目要求測資間保留一空白列。
    return "\n\n".join(outputs) + "\n"


def main() -> None:
    """命令列入口。"""

    raw = sys.stdin.read()
    sys.stdout.write(solve(raw))


if __name__ == "__main__":
    main()
