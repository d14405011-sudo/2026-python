import importlib.util
from pathlib import Path
import sys
import unittest


def load_hand_typed_module():
    file_path = Path(__file__).with_name("q10008-Hand-typed.py")
    spec = importlib.util.spec_from_file_location("q10008_hand_typed", file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q10008-Hand-typed.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mod = load_hand_typed_module()


class TestQ10008HandTyped(unittest.TestCase):
    def test_case_insensitive(self):
        raw = "1\nAaBbCc\n"
        self.assertEqual(mod.solve(raw), "A 2\nB 2\nC 2\n")

    def test_ignore_non_letters(self):
        raw = "2\nA1! a?\n12345\n"
        self.assertEqual(mod.solve(raw), "A 2\n")

    def test_sorting_rule(self):
        raw = "3\nAB\nBC\nCA\n"
        self.assertEqual(mod.solve(raw), "A 2\nB 2\nC 2\n")

    def test_mixed_frequency(self):
        raw = "2\nThis is a test\nWow!!\n"
        self.assertEqual(mod.solve(raw), "S 3\nT 3\nI 2\nW 2\nA 1\nE 1\nH 1\nO 1\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
