import subprocess
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent
Q = BASE / "q10101.py"
EASY = BASE / "q10101-easy.py"


def run_prog(path: Path, data: str) -> str:
    p = subprocess.run([sys.executable, str(path)], input=data, text=True, capture_output=True, check=True, cwd=str(BASE))
    return p.stdout.strip()


class TestQ10101(unittest.TestCase):
    SEGMENTS = {
        "0": frozenset("abcedf"),
        "1": frozenset("bc"),
        "2": frozenset("abdeg"),
        "3": frozenset("abcdg"),
        "4": frozenset("bcfg"),
        "5": frozenset("acdfg"),
        "6": frozenset("acdefg"),
        "7": frozenset("abc"),
        "8": frozenset("abcdefg"),
        "9": frozenset("abcdfg"),
        "+": frozenset("hv"),
        "-": frozenset("h"),
        "=": frozenset("xy"),
    }

    def _eval_expr(self, expr: str) -> int:
        self.assertTrue(expr, "expression must not be empty")
        total = 0
        number = ""
        op = "+"
        for ch in expr + "+":
            if ch.isdigit():
                number += ch
                continue
            self.assertTrue(number, f"invalid expression: {expr!r}")
            value = int(number)
            if op == "+":
                total += value
            else:
                total -= value
            self.assertIn(ch, "+-", f"unsupported operator {ch!r} in {expr!r}")
            op = ch
            number = ""
        return total

    def _assert_valid_solution(self, src: str, out: str) -> None:
        self.assertTrue(out.endswith("#"), f"solution must end with '#': {out!r}")
        src_core = src[:-1]
        out_core = out[:-1]
        self.assertEqual(out_core.count("="), 1, f"solution must contain exactly one '=': {out!r}")
        lhs, rhs = out_core.split("=")
        self.assertEqual(self._eval_expr(lhs), self._eval_expr(rhs), f"equation is not valid: {out!r}")

        self.assertEqual(len(src_core), len(out_core), "a one-match move must preserve character positions")
        src_segments = set()
        out_segments = set()
        for idx, ch in enumerate(src_core):
            self.assertIn(ch, self.SEGMENTS, f"unsupported source character {ch!r}")
            for seg in self.SEGMENTS[ch]:
                src_segments.add((idx, seg))
        for idx, ch in enumerate(out_core):
            self.assertIn(ch, self.SEGMENTS, f"unsupported output character {ch!r}")
            for seg in self.SEGMENTS[ch]:
                out_segments.add((idx, seg))

        self.assertEqual(len(src_segments), len(out_segments), "a one-match move must preserve match count")
        self.assertEqual(len(src_segments - out_segments), 1, f"expected exactly one removed match: {out!r}")
        self.assertEqual(len(out_segments - src_segments), 1, f"expected exactly one added match: {out!r}")

    def test_main(self) -> None:
        src = "1+1=3#"
        out = run_prog(Q, src + "\n")
        if out != "No":
            self._assert_valid_solution(src, out)

    def test_easy(self) -> None:
        src = "1+1=3#"
        out = run_prog(EASY, src + "\n")
        if out != "No":
            self._assert_valid_solution(src, out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
