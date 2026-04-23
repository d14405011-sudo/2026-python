import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10221_hand",
    pathlib.Path(__file__).parent / "q10221-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10221HandTyped(unittest.TestCase):
    def test_line_output(self):
        got = mod.solve_line(500, 30, "deg")
        left, right = map(float, got.split())
        self.assertAlmostEqual(left, 3633.775503, places=3)
        self.assertAlmostEqual(right, 3592.408346, places=3)


if __name__ == "__main__":
    unittest.main()
