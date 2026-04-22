from __future__ import annotations

import os
import subprocess
import sys
import unittest


def run_script(filename: str, input_data: str) -> str:
    """執行同資料夾下的解題程式，回傳標準輸出。"""
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


class TestQ10268(unittest.TestCase):
    def test_trials_and_limit(self) -> None:
        inp = "\n".join(
            [
                "1 1",
                "1 2",
                "2 100",
                "100 9223372036854775808",
                "0 0",
            ]
        ) + "\n"

        expected = "\n".join(
            [
                "1",
                "2",
                "14",
                "More than 63 trials needed.",
            ]
        )

        self.assertEqual(run_script("q10268.py", inp), expected)
        self.assertEqual(run_script("q10268-easy.py", inp), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
