"""question_10812.py / question_10812-easy.py 單元測試

測試重點：
- 合法輸入是否正確計算
- 無解情況是否正確回傳 impossible
- 兩個版本（標準版與 easy 版）是否輸出一致
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

# 取得目前測試檔所在目錄，方便載入同資料夾下的目標程式。
BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))


# easy 檔名含有減號，不能用一般 import，改用動態載入。
def load_easy_module():
    easy_path = BASE_DIR / "question_10812-easy.py"
    spec = importlib.util.spec_from_file_location("question_10812_easy", easy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法建立 question_10812-easy.py 的載入規格")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


from question_10812 import format_result, solve_case  # noqa: E402

EASY = load_easy_module()


class TestQuestion10812(unittest.TestCase):
    """UVA 10812 的核心邏輯測試。"""

    def test_valid_case_sample(self):
        """題目範例：40 20 -> 30 10。"""
        self.assertEqual(format_result(40, 20), "30 10")
        self.assertEqual(EASY.solve_one_case_easy(40, 20), "30 10")

    def test_impossible_when_diff_gt_sum(self):
        """差大於和：20 40 -> impossible。"""
        self.assertEqual(format_result(20, 40), "impossible")
        self.assertEqual(EASY.solve_one_case_easy(20, 40), "impossible")

    def test_impossible_when_odd_parity(self):
        """S + D 為奇數時，無法拆成兩個整數分數。"""
        self.assertEqual(format_result(11, 2), "impossible")
        self.assertEqual(EASY.solve_one_case_easy(11, 2), "impossible")

    def test_zero_zero(self):
        """邊界：0 0 -> 0 0。"""
        self.assertEqual(format_result(0, 0), "0 0")
        self.assertEqual(EASY.solve_one_case_easy(0, 0), "0 0")

    def test_same_scores(self):
        """分差為 0 時，兩隊同分。"""
        self.assertEqual(format_result(10, 0), "5 5")
        self.assertEqual(EASY.solve_one_case_easy(10, 0), "5 5")

    def test_large_numbers(self):
        """大數測試，確認仍正確。"""
        self.assertEqual(format_result(1_000_000, 2), "500001 499999")
        self.assertEqual(EASY.solve_one_case_easy(1_000_000, 2), "500001 499999")

    def test_solve_case_tuple(self):
        """標準版核心函式應回傳 tuple。"""
        self.assertEqual(solve_case(100, 20), (60, 40))

    def test_solve_case_none(self):
        """標準版核心函式在無解時回傳 None。"""
        self.assertIsNone(solve_case(5, 4))  # 5 + 4 = 9，奇數


if __name__ == "__main__":
    unittest.main(verbosity=2)
