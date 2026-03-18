"""QUESTION 948 單元測試。

測試重點：
1. 可唯一判定假幣時，應回傳正確編號。
2. 資訊不足或多解時，應回傳 0。
3. 多組測資輸出時，組間需有一空白列。
4. 標準版與 easy 版都需一致通過。
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    # 確保從專案根目錄執行 unittest 時，也能載入同資料夾下的解題檔。
    sys.path.insert(0, str(CURRENT_DIR))

from q948 import Weighing, detect_fake_coin, solve as solve_standard


def _load_easy_module():
    """動態載入檔名含連字號的 easy 版本模組。"""

    easy_path = Path(__file__).with_name("q948-easy.py")
    spec = importlib.util.spec_from_file_location("q948_easy", easy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q948-easy.py")

    module = importlib.util.module_from_spec(spec)
    # Python 3.14 下，dataclass 在處理型別註記時會透過 sys.modules 取模組。
    # 若未先註冊，可能導致 AttributeError。
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


easy_module = _load_easy_module()


class TestQuestion948Core(unittest.TestCase):
    """測試核心推論函式。"""

    def test_unique_by_balance_result(self) -> None:
        # '=' 出現過的硬幣都是真幣，因此此例唯一假幣是 3。
        weighings = [Weighing(left=[1], right=[2], result="=")]
        self.assertEqual(detect_fake_coin(3, weighings), 3)
        self.assertEqual(easy_module.detect_fake_coin_easy(3, weighings), 3)

    def test_ambiguous_should_return_zero(self) -> None:
        # 只有一個不平衡資訊，1(偏輕) 與 2(偏重) 都可能，應輸出 0。
        weighings = [Weighing(left=[1], right=[2], result="<")]
        self.assertEqual(detect_fake_coin(3, weighings), 0)
        self.assertEqual(easy_module.detect_fake_coin_easy(3, weighings), 0)

    def test_unique_heavy_coin(self) -> None:
        # 兩次秤重交叉後，只剩 coin 2 偏重能同時滿足。
        weighings = [
            Weighing(left=[1], right=[2], result="<"),
            Weighing(left=[2], right=[3], result=">")
        ]
        self.assertEqual(detect_fake_coin(4, weighings), 2)
        self.assertEqual(easy_module.detect_fake_coin_easy(4, weighings), 2)


class TestQuestion948IO(unittest.TestCase):
    """測試完整輸入輸出格式（包含空白列）。"""

    def test_multi_case_output_format(self) -> None:
        raw = (
            "2\n"
            "\n"
            "3 1\n"
            "1 1 2\n"
            "=\n"
            "\n"
            "3 1\n"
            "1 1 2\n"
            "<\n"
        )
        expected = "3\n\n0\n"
        self.assertEqual(solve_standard(raw), expected)
        self.assertEqual(easy_module.solve(raw), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
