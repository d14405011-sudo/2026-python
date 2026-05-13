import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10812_hand",
    pathlib.Path(__file__).parent / "q10812-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10812HandTyped(unittest.TestCase):
    def test_sample(self):
        src = "\n".join([
            "2",
            "40 20",
            "20 40",
        ])
        want = "\n".join([
            "30 10",
            "impossible",
        ])
        self.assertEqual(mod.solve_all(src), want)

    def test_more_cases(self):
        src = "\n".join([
            "4",
            "0 0",
            "10 0",
            "11 2",
            "1000000 2",
        ])
        want = "\n".join([
            "0 0",
            "5 5",
            "impossible",
            "500001 499999",
        ])
        self.assertEqual(mod.solve_all(src), want)

    def test_solve_case(self):
        self.assertEqual(mod.solve_case(100, 20), (60, 40))
        self.assertIsNone(mod.solve_case(5, 4))
        self.assertIsNone(mod.solve_case(20, 40))


if __name__ == "__main__":
    unittest.main()
