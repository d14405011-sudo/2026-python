import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10190",
    pathlib.Path(__file__).parent / "q10190.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10190(unittest.TestCase):
    def test_valid_cases(self):
        self.assertEqual(mod.solve_line(3, 3), "3 1")
        self.assertEqual(mod.solve_line(100, 10), "100 10 1")
        self.assertEqual(mod.solve_line(1, 2), "1")

    def test_boring_cases(self):
        self.assertEqual(mod.solve_line(34, 3), "Boring!")
        self.assertEqual(mod.solve_line(0, 2), "Boring!")
        self.assertEqual(mod.solve_line(10, 1), "Boring!")


if __name__ == "__main__":
    unittest.main()
