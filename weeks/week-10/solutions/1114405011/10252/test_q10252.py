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


class TestQ10252(unittest.TestCase):
    def test_odd_and_even_counts(self) -> None:
        # 測資1：三點共線，中位數唯一，答案為 4 1
        # 測資2：兩點 (0,0),(2,0)，x 在 [0,2] 都最佳，答案為 2 3
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

        expected = "\n".join(["4 1", "2 3"])

        self.assertEqual(run_script("q10252.py", inp), expected)
        self.assertEqual(run_script("q10252-easy.py", inp), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
