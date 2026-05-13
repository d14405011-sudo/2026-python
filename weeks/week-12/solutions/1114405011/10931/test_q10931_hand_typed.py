import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "q10931_hand",
    pathlib.Path(__file__).parent / "q10931-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10931HandTyped(unittest.TestCase):
    def test_sample(self):
        src = "\n".join(["1", "2", "10", "21", "0"])
        want = "\n".join([
            "The parity of 1 is 1 (mod 2).",
            "The parity of 10 is 1 (mod 2).",
            "The parity of 1010 is 2 (mod 2).",
            "The parity of 10101 is 3 (mod 2).",
        ])
        self.assertEqual(mod.solve_all(src), want)

    def test_single(self):
        self.assertEqual(mod.parity_line(21), "The parity of 10101 is 3 (mod 2).")


if __name__ == "__main__":
    unittest.main()
