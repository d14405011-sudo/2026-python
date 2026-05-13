import importlib.util
import pathlib
import unittest

from q10929 import is_multiple_of_11, solve_all

BASE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("q10929_easy", BASE / "q10929-easy.py")
mod_easy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod_easy)


class TestQ10929(unittest.TestCase):
    def test_multiple_check(self):
        self.assertTrue(is_multiple_of_11("11"))
        self.assertTrue(is_multiple_of_11("121"))
        self.assertFalse(is_multiple_of_11("112"))

        self.assertTrue(mod_easy.is_multiple_of_11_easy("11"))
        self.assertTrue(mod_easy.is_multiple_of_11_easy("121"))
        self.assertFalse(mod_easy.is_multiple_of_11_easy("112"))

    def test_solve_all(self):
        src = "\n".join(["112233", "121", "111112", "0"])
        want = "\n".join([
            "112233 is a multiple of 11.",
            "121 is a multiple of 11.",
            "111112 is not a multiple of 11.",
        ])
        self.assertEqual(solve_all(src), want)
        self.assertEqual(mod_easy.solve_all_easy(src), want)


if __name__ == "__main__":
    unittest.main()
