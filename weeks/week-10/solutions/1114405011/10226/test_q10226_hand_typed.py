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


class TestQ10226HandTyped(unittest.TestCase):
    def test_match_easy_multi_case(self) -> None:
        inp = "\n".join(
            [
                "2",
                "3",
                "0",
                "0",
                "0",
                "2",
                "1 0",
                "0",
            ]
        ) + "\n"
        easy = run_script("q10226-easy.py", inp)
        hand = run_script("q10226-Hand-typed.py", inp)
        self.assertEqual(hand, easy)

    def test_single_answer_case(self) -> None:
        inp = "2\n1 0\n0\n"
        expected = "BA"
        hand = run_script("q10226-Hand-typed.py", inp)
        self.assertEqual(hand, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
