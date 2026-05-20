import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Test11063HandTyped(unittest.TestCase):
    def test_hand(self) -> None:
        data = "1\n255 255 255\n"
        expected = "255.0000 255.0000 255.0000\nThe average of Y is 255.0000"
        p = subprocess.run(
            [sys.executable, str(BASE_DIR / "q11063-Hand-typed.py")],
            input=data,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(p.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
