import importlib.util
import pathlib
import unittest

from q10931 import format_line, parity_info, solve_all

BASE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("q10931_easy", BASE / "q10931-easy.py")
mod_easy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod_easy)


class TestQ10931(unittest.TestCase):
    def test_parity_info(self):
        self.assertEqual(parity_info(1), ("1", 1))
        self.assertEqual(parity_info(10), ("1010", 2))

        self.assertEqual(mod_easy.to_binary_and_ones_easy(1), ("1", 1))
        self.assertEqual(mod_easy.to_binary_and_ones_easy(10), ("1010", 2))

    def test_format_line(self):
        self.assertEqual(format_line(21), "The parity of 10101 is 3 (mod 2).")
        self.assertEqual(mod_easy.parity_line_easy(21), "The parity of 10101 is 3 (mod 2).")

    def test_solve_all(self):
        src = "\n".join(["1", "2", "10", "21", "0"])
        want = "\n".join([
            "The parity of 1 is 1 (mod 2).",
            "The parity of 10 is 1 (mod 2).",
            "The parity of 1010 is 2 (mod 2).",
            "The parity of 10101 is 3 (mod 2).",
        ])
        self.assertEqual(solve_all(src), want)
        self.assertEqual(mod_easy.solve_all_easy(src), want)


if __name__ == "__main__":
    unittest.main()
