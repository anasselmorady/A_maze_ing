from __future__ import annotations
from mazegen.maze import Maze
import sys


PATTERN_42 = [
    "1000111",
    "1000001",
    "1110111",
    "0010100",
    "0010111",
]


def _pattern_start(maze: Maze) -> tuple[int, int]:
    """Return the top-left position of the centered 42 pattern."""
    pattern_h = len(PATTERN_42)
    pattern_w = len(PATTERN_42[0])

    center_x = maze.width // 2
    center_y = maze.height // 2

    start_x = center_x - pattern_w // 2
    start_y = center_y - pattern_h // 2

    return start_x, start_y


def _entry_or_exit_inside_pattern(
        maze: Maze,
        start_x: int,
        start_y: int) -> None:
    """Raise an error if entry or exit is placed on a blocked 42 cell."""
    for py in range(len(PATTERN_42)):
        for px in range(len(PATTERN_42[0])):
            if PATTERN_42[py][px] != "1":
                continue

            x = start_x + px
            y = start_y + py

            if (x, y) == maze.entry:
                raise ValueError("ENTRY cannot be inside 42 pattern.")
            if (x, y) == maze.exit:
                raise ValueError("EXIT cannot be inside 42 pattern.")


def apply_42_pattern(maze: Maze) -> None:
    """Place 42 exactly in the center of the maze."""
    pattern_h = len(PATTERN_42)
    pattern_w = len(PATTERN_42[0])

    if maze.width < pattern_w + 2 or maze.height < pattern_h + 2:
        print("Warning: maze too small for 42 pattern.")
        sys.exit()

    start_x, start_y = _pattern_start(maze)
    _entry_or_exit_inside_pattern(maze, start_x, start_y)

    for py in range(pattern_h):
        for px in range(pattern_w):
            if PATTERN_42[py][px] != "1":
                continue

            x = start_x + px
            y = start_y + py

            if not maze.in_bounds(x, y):
                continue

            maze.grid[y][x].blocked = True
