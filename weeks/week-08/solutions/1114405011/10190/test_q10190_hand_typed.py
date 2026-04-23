import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10190_hand",
    pathlib.Path(__file__).parent / "q10190-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10190HandTyped(unittest.TestCase):
    def test_valid_and_boring(self):
        self.assertEqual(mod.solve_line(3, 3), "3 1")
        self.assertEqual(mod.solve_line(100, 10), "100 10 1")
        self.assertEqual(mod.solve_line(34, 3), "Boring!")


if __name__ == "__main__":
    unittest.main()
