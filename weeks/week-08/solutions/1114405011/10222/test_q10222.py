import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10222",
    pathlib.Path(__file__).parent / "q10222.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10222(unittest.TestCase):
    def test_phrase(self):
        self.assertEqual(mod.decode_line("O S, GOMR YPFSU/"), "I AM FINE TODAY.")

    def test_lowercase(self):
        self.assertEqual(mod.decode_line("o s"), "i a")


if __name__ == "__main__":
    unittest.main()
