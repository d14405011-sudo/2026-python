"""q10019 單元測試。

測試重點：
1. 基本差值計算。
2. 輸入大小順序互換時結果一致。
3. 可處理大整數。
4. 空行可忽略。
5. 標準版與 easy 版結果一致。
"""

import importlib.util
from pathlib import Path
import sys
import unittest


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import q10019


def load_easy_module():
    easy_path = Path(__file__).with_name("q10019-easy.py")
    spec = importlib.util.spec_from_file_location("q10019_easy", easy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q10019-easy.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


easy = load_easy_module()


class TestQ10019(unittest.TestCase):
    def test_basic(self):
        raw = "10 12\n"
        expected = "2\n"
        self.assertEqual(q10019.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_reverse_order(self):
        raw = "100 1\n1 100\n"
        expected = "99\n99\n"
        self.assertEqual(q10019.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_large_numbers(self):
        raw = "0 9223372036854775808\n"
        expected = "9223372036854775808\n"
        self.assertEqual(q10019.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_ignore_blank_lines(self):
        raw = "\n5 5\n\n7 2\n"
        expected = "0\n5\n"
        self.assertEqual(q10019.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
