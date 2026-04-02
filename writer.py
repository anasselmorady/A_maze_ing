from __future__ import annotations

from mazegen.maze import Maze


def cell_to_hex(maze: Maze, x: int, y: int) -> str:
    """Convert one cell walls to one hexadecimal digit."""
    cell = maze.grid[y][x]
    value = 0

    if cell.walls["N"]:
        value |= 1
    if cell.walls["E"]:
        value |= 2
    if cell.walls["S"]:
        value |= 4
    if cell.walls["W"]:
        value |= 8

    return format(value, "X")


def write_output(maze: Maze, filename: str, path: str) -> None:
    """Write maze output file."""
    with open(filename, "w", encoding="utf-8") as file:
        for y in range(maze.height):
            line = "".join(cell_to_hex(maze, x, y) for x in range(maze.width))
            file.write(line + "\n")

        file.write("\n")
        file.write(f"{maze.entry[0]},{maze.entry[1]}\n")
        file.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        file.write(path + "\n")
