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


class TestQ10252HandTyped(unittest.TestCase):
    def test_match_easy_and_known(self) -> None:
        inp = "\n".join(
            [
                "2",
                "3",
                "0 0",
                "1 1",
                "2 2",
                "2",
                "0 0",
                "2 0",
            ]
        ) + "\n"
        easy = run_script("q10252-easy.py", inp)
        hand = run_script("q10252-Hand-typed.py", inp)
        self.assertEqual(hand, easy)
        self.assertEqual(hand, "4 1\n2 3")


if __name__ == "__main__":
    unittest.main(verbosity=2)
