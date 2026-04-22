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


class TestQ10268HandTyped(unittest.TestCase):
    def test_match_easy_and_limit(self) -> None:
        inp = "\n".join(
            [
                "1 1",
                "1 2",
                "2 100",
                "100 9223372036854775808",
                "0 0",
            ]
        ) + "\n"
        easy = run_script("q10268-easy.py", inp)
        hand = run_script("q10268-Hand-typed.py", inp)
        self.assertEqual(hand, easy)
        self.assertEqual(hand, "1\n2\n14\nMore than 63 trials needed.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
