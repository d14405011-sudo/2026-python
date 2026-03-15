import unittest

from robot_core import RobotState, run_commands


class TestRobotScent(unittest.TestCase):
    def test_first_robot_leaves_scent_when_lost(self):
        scents = set()
        final_state, _ = run_commands(
            RobotState(5, 3, "N"),
            "F",
            width=5,
            height=3,
            scents=scents,
        )
        self.assertTrue(final_state.lost)
        self.assertIn((5, 3, "N"), scents)

    def test_second_robot_ignores_dangerous_move_with_same_scent(self):
        scents = set()
        run_commands(RobotState(5, 3, "N"), "F", 5, 3, scents)

        second_state, history = run_commands(
            RobotState(5, 3, "N"),
            "F",
            width=5,
            height=3,
            scents=scents,
        )
        self.assertFalse(second_state.lost)
        self.assertEqual((second_state.x, second_state.y, second_state.direction), (5, 3, "N"))
        self.assertEqual(history[-1].event, "SCENT_BLOCK")

    def test_scent_block_still_continues_next_instruction(self):
        scents = set()
        run_commands(RobotState(5, 3, "N"), "F", 5, 3, scents)

        # First F is blocked by scent, then R should still execute.
        second_state, history = run_commands(
            RobotState(5, 3, "N"),
            "FR",
            width=5,
            height=3,
            scents=scents,
        )
        self.assertFalse(second_state.lost)
        self.assertEqual((second_state.x, second_state.y, second_state.direction), (5, 3, "E"))
        self.assertEqual(history[0].event, "SCENT_BLOCK")
        self.assertEqual(history[1].event, "TURN")

    def test_same_cell_different_direction_does_not_share_scent(self):
        scents = set()
        run_commands(RobotState(5, 3, "N"), "F", 5, 3, scents)

        second_state, _ = run_commands(
            RobotState(5, 3, "E"),
            "F",
            width=5,
            height=3,
            scents=scents,
        )
        self.assertTrue(second_state.lost)

    def test_scent_key_includes_direction(self):
        scents = {(2, 2, "N")}
        state, _ = run_commands(
            RobotState(2, 2, "E"),
            "F",
            width=5,
            height=3,
            scents=scents,
        )
        self.assertEqual((state.x, state.y), (3, 2))
        self.assertFalse(state.lost)

    def test_typical_uva_sequence_sample_1(self):
        scents = set()

        s1, _ = run_commands(RobotState(1, 1, "E"), "RFRFRFRF", 5, 3, scents)
        s2, _ = run_commands(RobotState(3, 2, "N"), "FRRFLLFFRRFLL", 5, 3, scents)
        s3, _ = run_commands(RobotState(0, 3, "W"), "LLFFFLFLFL", 5, 3, scents)

        self.assertEqual((s1.x, s1.y, s1.direction, s1.lost), (1, 1, "E", False))
        self.assertEqual((s2.x, s2.y, s2.direction, s2.lost), (3, 3, "N", True))
        self.assertEqual((s3.x, s3.y, s3.direction, s3.lost), (2, 3, "S", False))

    def test_lost_robot_does_not_continue(self):
        scents = set()
        s, history = run_commands(RobotState(0, 0, "S"), "FFFF", 5, 3, scents)
        self.assertTrue(s.lost)
        self.assertEqual(len(history), 1)


if __name__ == "__main__":
    unittest.main()
