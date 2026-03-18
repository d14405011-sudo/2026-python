"""q10008 單元測試。

測試目標：
1. 驗證大小寫合併統計。
2. 驗證非字母字元不應被計數。
3. 驗證排序規則（次數降冪、字母升冪）。
4. 驗證標準版與 easy 版結果一致。
"""

import importlib.util
from pathlib import Path
import sys
import unittest


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import q10008


def load_easy_module():
    easy_path = Path(__file__).with_name("q10008-easy.py")
    spec = importlib.util.spec_from_file_location("q10008_easy", easy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q10008-easy.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


easy = load_easy_module()


class TestQ10008(unittest.TestCase):
    def test_case_insensitive(self):
        raw = "1\nAaBbCc\n"
        expected = "A 2\nB 2\nC 2\n"
        self.assertEqual(q10008.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_ignore_non_letters(self):
        raw = "2\nA1! a?\n12345\n"
        expected = "A 2\n"
        self.assertEqual(q10008.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_sorting_rule(self):
        raw = "3\nAB\nBC\nCA\n"
        # A/B/C 都是 2 次，需依字母序輸出。
        expected = "A 2\nB 2\nC 2\n"
        self.assertEqual(q10008.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_mixed_frequency(self):
        raw = "2\nThis is a test\nWow!!\n"
        expected = "S 3\nT 3\nI 2\nW 2\nA 1\nE 1\nH 1\nO 1\n"
        self.assertEqual(q10008.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
