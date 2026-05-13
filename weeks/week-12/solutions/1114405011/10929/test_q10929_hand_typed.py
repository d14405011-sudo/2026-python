import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "q10929_hand",
    pathlib.Path(__file__).parent / "q10929-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10929HandTyped(unittest.TestCase):
    def test_solve_all(self):
        src = "\n".join(["112233", "121", "111112", "0"])
        want = "\n".join([
            "112233 is a multiple of 11.",
            "121 is a multiple of 11.",
            "111112 is not a multiple of 11.",
        ])
        self.assertEqual(mod.solve_all(src), want)

    def test_check(self):
        self.assertTrue(mod.is_multiple_of_11("11"))
        self.assertFalse(mod.is_multiple_of_11("112"))


if __name__ == "__main__":
    unittest.main()
