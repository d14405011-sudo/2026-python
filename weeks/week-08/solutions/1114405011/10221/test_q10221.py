import importlib.util
import pathlib
import unittest


spec = importlib.util.spec_from_file_location(
    "q10221",
    pathlib.Path(__file__).parent / "q10221.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestQ10221(unittest.TestCase):
    def test_deg_and_min(self):
        arc, chord = mod.compute_distances(500, 30, "deg")
        self.assertAlmostEqual(arc, 3633.775503, places=3)
        self.assertAlmostEqual(chord, 3592.408346, places=3)

        arc2, chord2 = mod.compute_distances(700, 60, "min")
        self.assertAlmostEqual(arc2, 124.616509, places=3)
        self.assertAlmostEqual(chord2, 124.614927, places=3)

    def test_large_angle_fold(self):
        a1, c1 = mod.compute_distances(0, 200, "deg")
        a2, c2 = mod.compute_distances(0, 160, "deg")
        self.assertAlmostEqual(a1, a2, places=6)
        self.assertAlmostEqual(c1, c2, places=6)


if __name__ == "__main__":
    unittest.main()
