"""QUESTION 948 的 easy 版本（更好記憶）。

記憶口訣：
1. 先找真幣（所有 '=' 出現過的都是真幣）。
2. 再找嫌疑（有出現在 '<' 或 '>' 的，扣掉真幣）。
3. 逐一試演（每個嫌疑各試偏重、偏輕）。
4. 唯一答案（只有一顆成立才輸出，否則 0）。
"""

from typing import List, Tuple
import sys


def _parts(w):
    """把秤重資料統一轉成 (left, right, result) 三元組。

    這裡同時支援：
    - tuple/list: (left, right, result)
    - 物件型態: 具備 left/right/result 屬性（例如標準版 Weighing dataclass）
    """

    if isinstance(w, (tuple, list)) and len(w) == 3:
        return w[0], w[1], w[2]
    return w.left, w.right, w.result


def check_coin(coin: int, is_heavy: bool, weighings: List[Tuple[List[int], List[int], str]]) -> bool:
    """檢查某顆硬幣在指定狀態下（偏重或偏輕）是否符合全部秤重。

    參數說明：
    - coin: 假設中的假幣編號。
    - is_heavy: True 代表假幣偏重，False 代表假幣偏輕。
    - weighings: 每次秤重資料，格式為 (left, right, result)。
    """

    # 偏重用 +1 表示，偏輕用 -1 表示。
    # 之後可以統一用「左邊影響 - 右邊影響」來判斷結果。
    sign = 1 if is_heavy else -1

    for w in weighings:
        left, right, result = _parts(w)
        # 如果假幣在左盤，左盤受到 sign 影響；不在左盤就是 0。
        left_effect = sign if coin in left else 0
        # 如果假幣在右盤，右盤受到 sign 影響；不在右盤就是 0。
        right_effect = sign if coin in right else 0

        # diff 的意義：
        # diff > 0 代表左邊比較重
        # diff < 0 代表左邊比較輕
        # diff = 0 代表平衡
        diff = left_effect - right_effect

        # 逐一比對這次秤重的真實結果，不符合就直接失敗。
        if result == "=" and diff != 0:
            return False
        if result == "<" and diff >= 0:
            return False
        if result == ">" and diff <= 0:
            return False

    # 全部秤重都能解釋，代表此假設可行。
    return True


def detect_fake_coin_easy(n: int, weighings: List[Tuple[List[int], List[int], str]]) -> int:
    """回傳唯一可判定的假幣編號；若無法唯一判定則回傳 0。"""

    genuine = set()
    suspicious = set()

    for w in weighings:
        left, right, result = _parts(w)
        involved = set(left) | set(right)

        # 平衡：這次上秤的全部都是真幣。
        if result == "=":
            genuine |= involved
        # 不平衡：這次上秤的全部都先列入可疑。
        else:
            suspicious |= involved

    # 在平衡中出現過的一定是真幣，所以從可疑名單剔除。
    suspicious -= genuine

    # 若沒有任何不平衡可疑者，代表只剩「從未在 '=' 出現」的可能。
    if not suspicious:
        remain = [coin for coin in range(1, n + 1) if coin not in genuine]
        return remain[0] if len(remain) == 1 else 0

    possible = []
    for coin in sorted(suspicious):
        # 只要偏重或偏輕其中一種可成立，這顆就先保留。
        if check_coin(coin, True, weighings) or check_coin(coin, False, weighings):
            possible.append(coin)

    # 必須唯一，否則輸出 0。
    return possible[0] if len(possible) == 1 else 0


def solve(raw: str) -> str:
    """把整份輸入字串轉成題目要求的輸出字串。"""

    # 用 split() 可自動忽略空白行，最適合這題格式。
    tokens = raw.split()
    if not tokens:
        return ""

    idx = 0
    t = int(tokens[idx])
    idx += 1
    ans = []

    for _ in range(t):
        n = int(tokens[idx])
        k = int(tokens[idx + 1])
        idx += 2

        weighings = []

        for _ in range(k):
            p = int(tokens[idx])
            idx += 1

            left = list(map(int, tokens[idx: idx + p]))
            idx += p
            right = list(map(int, tokens[idx: idx + p]))
            idx += p

            result = tokens[idx]
            idx += 1

            weighings.append((left, right, result))

        ans.append(str(detect_fake_coin_easy(n, weighings)))

    # 題目要求：不同測資輸出間要有一個空白行。
    return "\n\n".join(ans) + "\n"


def main() -> None:
    raw = sys.stdin.read()
    sys.stdout.write(solve(raw))


if __name__ == "__main__":
    main()
