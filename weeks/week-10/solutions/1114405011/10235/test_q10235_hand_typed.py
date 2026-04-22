from __future__ import annotations

import os
import subprocess
import sys
import unittest


def run_script(filename: str, input_data: str) -> str:
    here = os.path.dirname(__file__)
    path = os.path.join(here, filename)
    proc = subprocess.run(
        [sys.executable, path],
        input=input_data,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout


class TestQ10235HandTyped(unittest.TestCase):
    def test_match_easy(self) -> None:
        inp = "\n".join(
            [
                "3",
                "1 1",
                "1",
                "2 2",
                "11",
                "11",
                "2 2",
                "10",
                "11",
            ]
        ) + "\n"
        easy = run_script("q10235-easy.py", inp)
        hand = run_script("q10235-Hand-typed.py", inp)
        self.assertEqual(hand, easy)


if __name__ == "__main__":
    unittest.main(verbosity=2)
