import importlib.util
from pathlib import Path
import sys
import unittest


def load_hand_typed_module():
    file_path = Path(__file__).with_name("q10035-Hand-typed.py")
    spec = importlib.util.spec_from_file_location("q10035_hand_typed", file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q10035-Hand-typed.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mod = load_hand_typed_module()


class TestQ10035HandTyped(unittest.TestCase):
    def test_no_carry(self):
        raw = "123 456\n0 0\n"
        self.assertEqual(mod.solve(raw), "No carry operation.\n")

    def test_one_carry(self):
        raw = "123 594\n0 0\n"
        self.assertEqual(mod.solve(raw), "1 carry operation.\n")

    def test_multiple_carries(self):
        raw = "555 555\n0 0\n"
        self.assertEqual(mod.solve(raw), "3 carry operations.\n")

    def test_stop_at_zero_zero(self):
        raw = "1 9\n0 0\n999 1\n"
        self.assertEqual(mod.solve(raw), "1 carry operation.\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
