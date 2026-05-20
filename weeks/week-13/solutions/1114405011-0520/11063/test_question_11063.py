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


class Test11063(unittest.TestCase):
    def test_small_image(self) -> None:
        data = "2\n255 0 0 0 255 0\n0 0 255 255 255 255\n"
        expected = "\n".join(
            [
                "131.2995 67.6770 6.3240",
                "82.7220 170.9520 31.8240",
                "40.9785 16.3710 216.8520",
                "255.0000 255.0000 255.0000",
                "The average of Y is 127.5000",
            ]
        )
        self.assertEqual(run("question_11063.py", data), expected)
        self.assertEqual(run("question_11063-easy.py", data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
