"""q10035 單元測試。

測試重點：
1. 0 次進位、1 次進位、多次進位。
2. 遇到 0 0 要停止，後續輸入不可再處理。
3. 標準版與 easy 版輸出必須一致。
"""

import importlib.util
from pathlib import Path
import sys
import unittest


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import q10035


def load_easy_module():
    easy_path = Path(__file__).with_name("q10035-easy.py")
    spec = importlib.util.spec_from_file_location("q10035_easy", easy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q10035-easy.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


easy = load_easy_module()


class TestQ10035(unittest.TestCase):
    def test_no_carry(self):
        raw = "123 456\n0 0\n"
        expected = "No carry operation.\n"
        self.assertEqual(q10035.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_one_carry(self):
        raw = "123 594\n0 0\n"
        expected = "1 carry operation.\n"
        self.assertEqual(q10035.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_multiple_carries(self):
        raw = "555 555\n0 0\n"
        expected = "3 carry operations.\n"
        self.assertEqual(q10035.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_stop_at_zero_zero(self):
        raw = "1 9\n0 0\n999 1\n"
        expected = "1 carry operation.\n"
        self.assertEqual(q10035.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
