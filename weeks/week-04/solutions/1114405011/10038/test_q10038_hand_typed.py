import importlib.util
from pathlib import Path
import sys
import unittest


def load_hand_typed_module():
    file_path = Path(__file__).with_name("q10038-Hand-typed.py")
    spec = importlib.util.spec_from_file_location("q10038_hand_typed", file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 q10038-Hand-typed.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mod = load_hand_typed_module()


class TestQ10038HandTyped(unittest.TestCase):
    def test_jolly(self):
        self.assertEqual(mod.solve("4 1 4 2 3\n"), "Jolly\n")

    def test_not_jolly(self):
        self.assertEqual(mod.solve("5 1 4 2 -1 6\n"), "Not jolly\n")

    def test_single_number(self):
        self.assertEqual(mod.solve("1 42\n"), "Jolly\n")

    def test_multiple_lines(self):
        raw = "4 1 4 2 3\n5 1 4 2 -1 6\n"
        self.assertEqual(mod.solve(raw), "Jolly\nNot jolly\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
