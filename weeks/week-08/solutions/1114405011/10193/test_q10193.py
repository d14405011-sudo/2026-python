import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10193",
    pathlib.Path(__file__).parent / "q10193.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10193(unittest.TestCase):
    def test_cases(self):
        src = "\n".join([
            "2",
            "1100",
            "1010",
            "1",
            "10",
        ])
        want = "\n".join([
            "Pair #1: All you need is love!",
            "Pair #2: Love is not all you need!",
        ])
        self.assertEqual(mod.solve_all(src), want)


if __name__ == "__main__":
    unittest.main()
