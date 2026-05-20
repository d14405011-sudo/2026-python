import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Test11150HandTyped(unittest.TestCase):
    def test_hand(self) -> None:
        data = "10\n2 3 3\n2 5 8\n"
        p = subprocess.run(
            [sys.executable, str(BASE_DIR / "q11150-Hand-typed.py")],
            input=data,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(p.stdout.strip(), "0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
