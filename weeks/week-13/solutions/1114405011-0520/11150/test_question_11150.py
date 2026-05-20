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


class Test11150(unittest.TestCase):
    def test_fixed_jump(self) -> None:
        data = "10\n2 2 3\n2 3 6\n"
        # 只能落在 2,4,6,8,10，會踩到 2 與 6，共 2 顆。
        expected = "2"
        self.assertEqual(run("question_11150.py", data), expected)
        self.assertEqual(run("question_11150-easy.py", data), expected)

    def test_range_jump(self) -> None:
        data = "10\n2 3 3\n2 5 8\n"
        # 可走 0->3->6->9->11，不踩任何石頭。
        expected = "0"
        self.assertEqual(run("question_11150.py", data), expected)
        self.assertEqual(run("question_11150-easy.py", data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
