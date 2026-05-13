import importlib.util
import pathlib
import unittest

from q10908 import largest_square_size, solve_all

BASE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("q10908_easy", BASE / "q10908-easy.py")
mod_easy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod_easy)


class TestQ10908(unittest.TestCase):
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
        self.assertEqual(solve_all(src), want)
        self.assertEqual(mod_easy.solve_all_easy(src), want)

    def test_all_same_center(self):
        g = [
            "aaaaa",
            "aaaaa",
            "aaaaa",
            "aaaaa",
            "aaaaa",
        ]
        self.assertEqual(largest_square_size(g, 2, 2), 5)
        self.assertEqual(mod_easy.largest_square_size_easy(g, 2, 2), 5)

    def test_corner_only_one(self):
        g = [
            "aaaaa",
            "aaaaa",
            "aaaaa",
            "aaaaa",
            "aaaaa",
        ]
        self.assertEqual(largest_square_size(g, 0, 0), 1)
        self.assertEqual(mod_easy.largest_square_size_easy(g, 0, 0), 1)


if __name__ == "__main__":
    unittest.main()
