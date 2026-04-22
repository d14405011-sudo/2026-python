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


class TestQ10242(unittest.TestCase):
    def test_sample_like_case(self) -> None:
        # 使用題意常見示例，最大可搶為 47。
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

        expected = "47"

        self.assertEqual(run_script("q10242.py", inp), expected)
        self.assertEqual(run_script("q10242-easy.py", inp), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
