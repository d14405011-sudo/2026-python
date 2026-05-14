import importlib.util
import pathlib
import unittest

from q10922 import nine_degree, solve_all

BASE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("q10922_easy", BASE / "q10922-easy.py")
mod_easy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod_easy)


class TestQ10922(unittest.TestCase):
    def test_nine_degree_values(self):
        self.assertEqual(nine_degree("9"), 1)
        self.assertEqual(nine_degree("999"), 2)
        self.assertEqual(nine_degree("18"), 2)
        self.assertIsNone(nine_degree("10"))

        self.assertEqual(mod_easy.nine_degree_easy("9"), 1)
        self.assertEqual(mod_easy.nine_degree_easy("999"), 2)
        self.assertEqual(mod_easy.nine_degree_easy("18"), 2)
        self.assertIsNone(mod_easy.nine_degree_easy("10"))

    def test_solve_all(self):
        src = "\n".join(["999", "189", "18", "10", "0"])
        want = "\n".join([
            "9-degree of 999 is 2.",
            "9-degree of 189 is 2.",
            "9-degree of 18 is 2.",
            "10 is not a multiple of 9.",
        ])
        self.assertEqual(solve_all(src), want)
        self.assertEqual(mod_easy.solve_all_easy(src), want)


if __name__ == "__main__":
    unittest.main()
