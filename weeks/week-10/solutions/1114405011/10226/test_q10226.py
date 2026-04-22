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


class TestQ10226(unittest.TestCase):
    def test_all_permutations_no_ban(self) -> None:
        # N=3 且每個人都沒有禁位，合法排列共有 6 個。
        # 壓縮輸出規則：第一行完整輸出，後續只輸出與前一筆不同後綴。
        inp = "3\n0\n0\n0\n"
        expected = "\n".join(["ABC", "CB", "BAC", "CA", "CAB", "BA"])

        self.assertEqual(run_script("q10226.py", inp), expected)
        self.assertEqual(run_script("q10226-easy.py", inp), expected)

    def test_with_forbidden_position(self) -> None:
        # A 不可站 1 號位，所以只有 BA 一種。
        inp = "2\n1 0\n0\n"
        expected = "BA"

        self.assertEqual(run_script("q10226.py", inp), expected)
        self.assertEqual(run_script("q10226-easy.py", inp), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
