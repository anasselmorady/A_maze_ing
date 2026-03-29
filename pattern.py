from __future__ import annotations

from maze import Maze


PATTERN_42 = [
    "01000111",
    "01000001",
    "01110111",
    "00010100",
    "00010111",
]


def apply_42_pattern(maze: Maze) -> None:
    """Place 42 exactly in the center of the maze."""

    pattern_h = len(PATTERN_42)
    pattern_w = len(PATTERN_42[0])

    if maze.width < pattern_w + 2 or maze.height < pattern_h + 2:
        print("Warning: maze too small for 42 pattern.")
        return

    # center of maze
    center_x = maze.width // 2
    center_y = maze.height // 2

    # start position (centered)
    start_x = center_x - pattern_w // 2
    start_y = center_y - pattern_h // 2

    for py in range(pattern_h):
        for px in range(pattern_w):
            if PATTERN_42[py][px] != "1":
                continue

            x = start_x + px
            y = start_y + py

            if not maze.in_bounds(x, y):
                continue

            # لا تضع pattern فوق entry/exit
            if (x, y) == maze.entry or (x, y) == maze.exit:
                continue

            maze.grid[y][x].blocked = True
