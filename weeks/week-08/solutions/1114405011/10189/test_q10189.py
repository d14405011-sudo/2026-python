import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10189",
    pathlib.Path(__file__).parent / "q10189.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10189(unittest.TestCase):
    def test_sample(self):
        src = "\n".join([
            "4 4",
            "*...",
            "....",
            ".*..",
            "....",
            "3 5",
            "**...",
            ".....",
            ".*...",
            "0 0",
        ])
        want = "\n".join([
            "Field #1:",
            "*100",
            "2210",
            "1*10",
            "1110",
            "",
            "Field #2:",
            "**100",
            "33200",
            "1*100",
        ])
        self.assertEqual(mod.solve_all(src), want)

    def test_single(self):
        self.assertEqual(mod.solve_field(["."]), ["0"])
        self.assertEqual(mod.solve_field(["*"]), ["*"])


if __name__ == "__main__":
    unittest.main()
