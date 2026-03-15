"""Core logic for Robot Lost (UVA 118 style).

This module is intentionally independent from pygame so it can be unit tested.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

Direction = str
Scent = Tuple[int, int, Direction]

DIRECTIONS: Tuple[Direction, ...] = ("N", "E", "S", "W")
MOVE_DELTAS: Dict[Direction, Tuple[int, int]] = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}
VALID_COMMANDS = {"L", "R", "F"}


@dataclass(frozen=True)
class RobotState:
    x: int
    y: int
    direction: Direction
    lost: bool = False


@dataclass(frozen=True)
class StepResult:
    state: RobotState
    event: str


def validate_direction(direction: Direction) -> None:
    if direction not in DIRECTIONS:
        raise ValueError(f"Invalid direction: {direction}")


def validate_command(command: str) -> None:
    if command not in VALID_COMMANDS:
        raise ValueError(f"Invalid command: {command}")


def validate_grid_size(width: int, height: int) -> None:
    if width < 0 or height < 0:
        raise ValueError(f"Invalid grid size: width={width}, height={height}")


def in_bounds(x: int, y: int, width: int, height: int) -> bool:
    return 0 <= x <= width and 0 <= y <= height


def turn_left(direction: Direction) -> Direction:
    validate_direction(direction)
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx - 1) % 4]


def turn_right(direction: Direction) -> Direction:
    validate_direction(direction)
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx + 1) % 4]


def execute_instruction(
    state: RobotState,
    instruction: str,
    width: int,
    height: int,
    scents: Set[Scent],
) -> StepResult:
    """Execute one instruction and return new state + event.

    Events:
    - "TURN": successful L/R turn
    - "MOVE": successful forward move
    - "SCENT_BLOCK": dangerous F ignored due to scent
    - "LOST": robot moved out of bounds and is lost
    - "NOOP_LOST": robot already lost so instruction is ignored
    """
    validate_grid_size(width, height)
    validate_direction(state.direction)
    validate_command(instruction)

    if state.lost:
        return StepResult(state=state, event="NOOP_LOST")

    if instruction == "L":
        return StepResult(
            state=RobotState(state.x, state.y, turn_left(state.direction), False),
            event="TURN",
        )

    if instruction == "R":
        return StepResult(
            state=RobotState(state.x, state.y, turn_right(state.direction), False),
            event="TURN",
        )

    dx, dy = MOVE_DELTAS[state.direction]
    next_x, next_y = state.x + dx, state.y + dy

    if in_bounds(next_x, next_y, width, height):
        return StepResult(
            state=RobotState(next_x, next_y, state.direction, False),
            event="MOVE",
        )

    scent_key = (state.x, state.y, state.direction)
    if scent_key in scents:
        return StepResult(state=state, event="SCENT_BLOCK")

    scents.add(scent_key)
    return StepResult(
        state=RobotState(state.x, state.y, state.direction, True),
        event="LOST",
    )


def run_commands(
    initial_state: RobotState,
    commands: str,
    width: int,
    height: int,
    scents: Set[Scent],
) -> Tuple[RobotState, List[StepResult]]:
    """Run a command sequence until complete or robot is lost."""
    validate_grid_size(width, height)
    validate_direction(initial_state.direction)

    state = initial_state
    history: List[StepResult] = []

    for cmd in commands:
        step = execute_instruction(state, cmd, width, height, scents)
        history.append(step)
        state = step.state
        if state.lost:
            break

    return state, history
