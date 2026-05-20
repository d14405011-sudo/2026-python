import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Test11005HandTyped(unittest.TestCase):
    def test_hand_typed(self) -> None:
        costs = [1] * 36
        data = "\n".join(
            [
                "1",
                " ".join(map(str, costs[0:9])),
                " ".join(map(str, costs[9:18])),
                " ".join(map(str, costs[18:27])),
                " ".join(map(str, costs[27:36])),
                "1",
                "31",
            ]
        )
        expected = "Case 1:\nCheapest base(s) for number 31: 32 33 34 35 36"
        proc = subprocess.run(
            [sys.executable, str(BASE_DIR / "q11005-Hand-typed.py")],
            input=data,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(proc.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
