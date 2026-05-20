import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Test11332HandTyped(unittest.TestCase):
    def test_hand(self) -> None:
        data = "1\n1 0 2 0\n0\n"
        p = subprocess.run(
            [sys.executable, str(BASE_DIR / "q11332-Hand-typed.py")],
            input=data,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(p.stdout.strip(), "1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
