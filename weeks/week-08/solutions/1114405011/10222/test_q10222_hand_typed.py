import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10222_hand",
    pathlib.Path(__file__).parent / "q10222-Hand-typed.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10222HandTyped(unittest.TestCase):
    def test_phrase(self):
        self.assertEqual(mod.decode_line("O S, GOMR YPFSU/"), "I AM FINE TODAY.")


if __name__ == "__main__":
    unittest.main()
