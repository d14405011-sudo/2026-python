"""Headlessly render a demo replay.gif showing the scent mechanic."""
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from robot_game import Game


def main() -> None:
    game = Game()

    # Robot 1: march north until LOST at (0,3,N)
    for cmd in ["F", "F", "F", "F"]:
        game.apply_command(cmd)

    # Robot 2: same route — scent blocks the fatal F, then turns east and walks on
    game.reset_robot()
    for cmd in ["F", "F", "F", "F", "R", "F", "F", "F"]:
        game.apply_command(cmd)

    game.export_replay_gif()
    print(f"Done — {len(game.current_track)} frames written to assets/replay.gif")


if __name__ == "__main__":
    main()
