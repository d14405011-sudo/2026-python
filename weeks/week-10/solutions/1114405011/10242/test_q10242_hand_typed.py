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


class TestQ10242HandTyped(unittest.TestCase):
    def test_match_easy_and_known(self) -> None:
        inp = "\n".join(
            [
                "6 7",
                "1 2",
                "2 3",
                "3 5",
                "2 4",
                "4 1",
                "2 6",
                "6 5",
                "10",
                "12",
                "8",
                "16",
                "1",
                "5",
                "1 1",
                "5",
            ]
        ) + "\n"
        easy = run_script("q10242-easy.py", inp)
        hand = run_script("q10242-Hand-typed.py", inp)
        self.assertEqual(hand, easy)
        self.assertEqual(hand, "47")


if __name__ == "__main__":
    unittest.main(verbosity=2)
