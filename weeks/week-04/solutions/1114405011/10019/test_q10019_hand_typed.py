import importlib.util
from pathlib import Path
import sys
import unittest


def load_hand_typed_module():
    file_path = Path(__file__).with_name("q10019-Hand-typed.py")
    spec = importlib.util.spec_from_file_location("q10019_hand_typed", file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q10019-Hand-typed.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mod = load_hand_typed_module()


class TestQ10019HandTyped(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(mod.solve("10 12\n"), "2\n")

    def test_reverse_order(self):
        self.assertEqual(mod.solve("100 1\n1 100\n"), "99\n99\n")

    def test_large_numbers(self):
        self.assertEqual(mod.solve("0 9223372036854775808\n"), "9223372036854775808\n")

    def test_ignore_blank_lines(self):
        self.assertEqual(mod.solve("\n5 5\n\n7 2\n"), "0\n5\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
