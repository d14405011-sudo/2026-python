import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10193_hand",
    pathlib.Path(__file__).parent / "q10193-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10193HandTyped(unittest.TestCase):
    def test_cases(self):
        self.assertEqual(
            mod.solve_case("1100", "1010", 1),
            "Pair #1: All you need is love!",
        )
        self.assertEqual(
            mod.solve_case("1", "10", 2),
            "Pair #2: Love is not all you need!",
        )


if __name__ == "__main__":
    unittest.main()
