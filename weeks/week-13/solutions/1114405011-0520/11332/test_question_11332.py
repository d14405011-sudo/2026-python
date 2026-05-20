import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def run(name: str, inp: str) -> str:
    p = subprocess.run(
        [sys.executable, str(BASE_DIR / name)],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return p.stdout.strip()


class Test11332(unittest.TestCase):
    def test_parallel_segments(self) -> None:
        # 同一條射線上的兩段，近的可見、遠的被擋。
        data = "2\n1 1 2 2\n3 3 4 4\n0\n"
        expected = "1 0"
        self.assertEqual(run("question_11332.py", data), expected)
        self.assertEqual(run("question_11332-easy.py", data), expected)

    def test_separate_directions(self) -> None:
        data = "2\n1 1 2 2\n-2 1 -1 2\n0\n"
        expected = "1 1"
        self.assertEqual(run("question_11332.py", data), expected)
        self.assertEqual(run("question_11332-easy.py", data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
