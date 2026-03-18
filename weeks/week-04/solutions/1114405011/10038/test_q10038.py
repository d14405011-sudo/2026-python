"""q10038 單元測試。

測試重點：
1. 標準 Jolly 範例。
2. Not jolly 範例。
3. 單一元素序列。
4. 多組輸入時逐行輸出。
5. 標準版與 easy 版一致。
"""

import importlib.util
from pathlib import Path
import sys
import unittest


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import q10038


def load_easy_module():
    easy_path = Path(__file__).with_name("q10038-easy.py")
    spec = importlib.util.spec_from_file_location("q10038_easy", easy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q10038-easy.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


easy = load_easy_module()


class TestQ10038(unittest.TestCase):
    def test_jolly_sample_like(self):
        raw = "4 1 4 2 3\n"
        expected = "Jolly\n"
        self.assertEqual(q10038.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_not_jolly_sample_like(self):
        raw = "5 1 4 2 -1 6\n"
        expected = "Not jolly\n"
        self.assertEqual(q10038.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_single_number_is_jolly(self):
        raw = "1 999\n"
        expected = "Jolly\n"
        self.assertEqual(q10038.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)

    def test_multiple_lines(self):
        raw = "4 1 4 2 3\n5 1 4 2 -1 6\n"
        expected = "Jolly\nNot jolly\n"
        self.assertEqual(q10038.solve(raw), expected)
        self.assertEqual(easy.solve(raw), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
