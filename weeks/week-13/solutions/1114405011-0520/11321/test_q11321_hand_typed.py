import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Test11321HandTyped(unittest.TestCase):
    def test_hand(self) -> None:
        data = "2 3 2\n0 1\n1 1\n"
        expected = "<(_ _)>\n>_<"
        p = subprocess.run(
            [sys.executable, str(BASE_DIR / "q11321-Hand-typed.py")],
            input=data,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(p.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
