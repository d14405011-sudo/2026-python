import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "q10908_hand",
    pathlib.Path(__file__).parent / "q10908-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10908HandTyped(unittest.TestCase):
    def test_sample(self):
        src = "\n".join([
            "1",
            "7 10 4",
            "abbbaaaaaa",
            "abbbaaaaaa",
            "abbbaaaaaa",
            "aaaaaaaaaa",
            "aaaaaaaaaa",
            "aaccaaaaaa",
            "aaccaaaaaa",
            "1 2",
            "2 4",
            "4 6",
            "5 2",
        ])
        want = "\n".join([
            "7 10 4",
            "3",
            "1",
            "5",
            "1",
        ])
        self.assertEqual(mod.solve_all(src), want)

    def test_basic(self):
        g = ["aaa", "aaa", "aaa"]
        self.assertEqual(mod.largest_square_size(g, 1, 1), 3)


if __name__ == "__main__":
    unittest.main()
