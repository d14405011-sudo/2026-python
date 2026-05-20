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


class Test11321(unittest.TestCase):
    def test_line_grid(self) -> None:
        # 1x4 只剩單一路徑，封中間會失敗。
        data = "1 4 3\n0 1\n0 2\n0 3\n"
        expected = ">_<\n>_<\n>_<"
        self.assertEqual(run("question_11321.py", data), expected)
        self.assertEqual(run("question_11321-easy.py", data), expected)

    def test_two_rows(self) -> None:
        data = "2 3 2\n0 1\n1 1\n"
        # 先封第一列中間可行，第二列中間再封就斷路，應拒絕。
        expected = "<(_ _)>\n>_<"
        self.assertEqual(run("question_11321.py", data), expected)
        self.assertEqual(run("question_11321-easy.py", data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
