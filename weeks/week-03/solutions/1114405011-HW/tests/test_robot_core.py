import unittest

from robot_core import RobotState, run_commands, turn_left, turn_right


class TestRobotCore(unittest.TestCase):
    def test_turn_left_from_north(self):
        self.assertEqual(turn_left("N"), "W")

    def test_turn_right_from_north(self):
        self.assertEqual(turn_right("N"), "E")

    def test_four_right_turns_back_to_origin_direction(self):
        direction = "N"
        for _ in range(4):
            direction = turn_right(direction)
        self.assertEqual(direction, "N")

    def test_move_inside_boundary(self):
        scents = set()
        final_state, history = run_commands(
            RobotState(1, 1, "N"),
            "F",
            width=5,
            height=3,
            scents=scents,
        )
        self.assertEqual((final_state.x, final_state.y, final_state.direction), (1, 2, "N"))
        self.assertFalse(final_state.lost)
        self.assertEqual(history[-1].event, "MOVE")

    def test_lost_stops_following_commands(self):
        scents = set()
        final_state, history = run_commands(
            RobotState(0, 3, "N"),
            "FRF",
            width=5,
            height=3,
            scents=scents,
        )
        self.assertTrue(final_state.lost)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].event, "LOST")

    def test_invalid_instruction_raises(self):
        scents = set()
        with self.assertRaises(ValueError):
            run_commands(RobotState(0, 0, "N"), "X", 5, 3, scents)

    def test_invalid_initial_direction_raises(self):
        scents = set()
        with self.assertRaises(ValueError):
            run_commands(RobotState(0, 0, "A"), "F", 5, 3, scents)

    def test_negative_grid_size_raises(self):
        scents = set()
        with self.assertRaises(ValueError):
            run_commands(RobotState(0, 0, "N"), "F", -1, 3, scents)


if __name__ == "__main__":
    unittest.main()
