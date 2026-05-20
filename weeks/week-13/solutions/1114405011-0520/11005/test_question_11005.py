import random
import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def ref_cost(n: int, b: int, c: list[int]) -> int:
    if n == 0:
        return c[0]
    s = 0
    while n > 0:
        s += c[n % b]
        n //= b
    return s


def ref_solve(text: str) -> str:
    a = list(map(int, text.split()))
    i = 0
    t = a[i]
    i += 1
    out = []

    for cs in range(1, t + 1):
        c = a[i : i + 36]
        i += 36
        q = a[i]
        i += 1
        out.append(f"Case {cs}:")

        for _ in range(q):
            n = a[i]
            i += 1
            arr = [(b, ref_cost(n, b, c)) for b in range(2, 37)]
            m = min(v for _, v in arr)
            best = [b for b, v in arr if v == m]
            out.append(f"Cheapest base(s) for number {n}: " + " ".join(map(str, best)))

        if cs != t:
            out.append("")

    return "\n".join(out)


def run_file(file_name: str, inp: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(BASE_DIR / file_name)],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout.strip()


class Test11005(unittest.TestCase):
    def test_fixed(self) -> None:
        costs = [1] * 36
        data = "\n".join(
            [
                "1",
                " ".join(map(str, costs[0:9])),
                " ".join(map(str, costs[9:18])),
                " ".join(map(str, costs[18:27])),
                " ".join(map(str, costs[27:36])),
                "3",
                "0",
                "10",
                "31",
            ]
        )
        expected = ref_solve(data)
        self.assertEqual(run_file("question_11005.py", data), expected)
        self.assertEqual(run_file("question_11005-easy.py", data), expected)

    def test_random(self) -> None:
        random.seed(11005)
        lines = ["2"]
        for _ in range(2):
            costs = [random.randint(1, 9) for _ in range(36)]
            for i in range(0, 36, 9):
                lines.append(" ".join(map(str, costs[i : i + 9])))
            lines.append("4")
            for _ in range(4):
                lines.append(str(random.randint(0, 2_000_000_000)))
        data = "\n".join(lines)
        expected = ref_solve(data)
        self.assertEqual(run_file("question_11005.py", data), expected)
        self.assertEqual(run_file("question_11005-easy.py", data), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
