import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "q10922_hand",
    pathlib.Path(__file__).parent / "q10922-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10922HandTyped(unittest.TestCase):
    def test_sample_like(self):
        src = "\n".join(["999", "189", "10", "0"])
        want = "\n".join([
            "9-degree of 999 is 2.",
            "9-degree of 189 is 2.",
            "10 is not a multiple of 9.",
        ])
        self.assertEqual(mod.solve_all(src), want)

    def test_degree(self):
        self.assertEqual(mod.nine_degree("9"), 1)
        self.assertEqual(mod.nine_degree("18"), 1)
        self.assertEqual(mod.nine_degree("999"), 2)
        self.assertIsNone(mod.nine_degree("10"))


if __name__ == "__main__":
    unittest.main()
