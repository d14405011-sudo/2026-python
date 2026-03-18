import importlib.util
from pathlib import Path
import sys
import unittest


def load_hand_typed_module():
    file_path = Path(__file__).with_name("q948-Hand-typed.py")
    spec = importlib.util.spec_from_file_location("q948_hand_typed", file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q948-Hand-typed.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mod = load_hand_typed_module()


class TestQ948HandTyped(unittest.TestCase):
    def test_single_balance_unique(self):
        raw = "1\n\n3 1\n1 1 2\n=\n"
        self.assertEqual(mod.solve(raw), "3\n")

    def test_single_ambiguous(self):
        raw = "1\n\n3 1\n1 1 2\n<\n"
        self.assertEqual(mod.solve(raw), "0\n")

    def test_unique_heavy(self):
        raw = "1\n\n4 2\n1 1 2\n<\n1 2 3\n>\n"
        self.assertEqual(mod.solve(raw), "2\n")

    def test_multi_case_format(self):
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
        self.assertEqual(mod.solve(raw), "3\n\n0\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
