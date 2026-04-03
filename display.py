from __future__ import annotations

import os

from mazegen.maze import DIRS, Maze
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver
from writer import write_output


BLACK = "\033[48;5;0m  \033[0m"
WHITE = "\033[48;5;255m  \033[0m"
LIGHT_GRAY = "\033[48;5;252m  \033[0m"
MAGENTA = "\033[48;5;201m  \033[0m"
RED = "\033[48;5;196m  \033[0m"
CYAN = "\033[48;5;51m  \033[0m"
GREEN = "\033[48;5;46m  \033[0m"
YELLOW = "\033[48;5;226m  \033[0m"
BLUE = "\033[48;5;27m  \033[0m"
ORANGE = "\033[48;5;208m  \033[0m"

PALETTES = [
    {
        "wall": WHITE,
        "empty": BLACK,
        "entry": MAGENTA,
        "exit": RED,
        "path": CYAN,
        "pattern": LIGHT_GRAY,
        "current": ORANGE,
        "visited": BLUE,
    },
    {
        "wall": YELLOW,
        "empty": BLACK,
        "entry": MAGENTA,
        "exit": RED,
        "path": CYAN,
        "pattern": LIGHT_GRAY,
        "current": ORANGE,
        "visited": BLUE,
    },
    {
        "wall": GREEN,
        "empty": BLACK,
        "entry": BLUE,
        "exit": RED,
        "path": YELLOW,
        "pattern": LIGHT_GRAY,
        "current": ORANGE,
        "visited": CYAN,
    },
]


def clear_screen() -> None:
    """Clear terminal."""
    os.system("clear")


def build_display_grid(maze: Maze) -> list[list[str]]:
    """Build terminal display grid."""
    display_h = maze.height * 2 + 1
    display_w = maze.width * 2 + 1
    display = [["wall" for _ in range(display_w)] for _ in range(display_h)]

    for y in range(maze.height):
        for x in range(maze.width):
            dy = y * 2 + 1
            dx = x * 2 + 1
            cell = maze.grid[y][x]

            if cell.blocked:
                display[dy][dx] = "pattern"
                continue

            display[dy][dx] = "empty"

            if not cell.walls["N"]:
                display[dy - 1][dx] = "empty"
            if not cell.walls["S"]:
                display[dy + 1][dx] = "empty"
            if not cell.walls["W"]:
                display[dy][dx - 1] = "empty"
            if not cell.walls["E"]:
                display[dy][dx + 1] = "empty"

    return display


def path_cells(maze: Maze, path: str) -> list[tuple[int, int]]:
    """Convert path string to ordered cell positions."""
    x, y = maze.entry
    result = [(x, y)]

    for move in path:
        dx, dy = DIRS[move]
        x += dx
        y += dy
        result.append((x, y))

    return result


def apply_path_overlay(
        maze: Maze,
        display: list[list[str]],
        path: str
        ) -> None:
    """Overlay shortest path."""
    ordered_cells = path_cells(maze, path)

    for i in range(len(ordered_cells) - 1):
        x1, y1 = ordered_cells[i]
        x2, y2 = ordered_cells[i + 1]

        gx1 = x1 * 2 + 1
        gy1 = y1 * 2 + 1
        gx2 = x2 * 2 + 1
        gy2 = y2 * 2 + 1

        mx = (gx1 + gx2) // 2
        my = (gy1 + gy2) // 2

        if (x1, y1) != maze.entry and (x1, y1) != maze.exit:
            display[gy1][gx1] = "path"

        display[my][mx] = "path"

    last_x, last_y = ordered_cells[-1]
    if (last_x, last_y) != maze.entry and (last_x, last_y) != maze.exit:
        display[last_y * 2 + 1][last_x * 2 + 1] = "path"


def apply_entry_exit(maze: Maze, display: list[list[str]]) -> None:
    """Overlay entry and exit."""
    ex, ey = maze.entry
    xx, xy = maze.exit
    display[ey * 2 + 1][ex * 2 + 1] = "entry"
    display[xy * 2 + 1][xx * 2 + 1] = "exit"


def render_pretty(
        maze: Maze,
        show_path: bool,
        path: str | None,
        palette_index: int
        ) -> None:
    """Render maze in terminal."""
    palette = PALETTES[palette_index % len(PALETTES)]
    display = build_display_grid(maze)

    if show_path and path is not None:
        apply_path_overlay(maze, display, path)

    apply_entry_exit(maze, display)

    for row in display:
        line = ""
        for cell in row:
            line += palette.get(cell, palette["empty"])
        print(line)


def interactive_menu(
    maze: Maze,
    generator: MazeGenerator,
    solver: MazeSolver,
    output_file: str,
) -> None:
    """Run terminal interaction loop."""
    show_path = False
    palette_index = 0

    while True:
        path = solver.shortest_path()
        write_output(maze, output_file, path)

        clear_screen()
        print("bash-3.2$ python3 ./a_maze_ing.py config.txt\n")
        render_pretty(maze, show_path, path, palette_index)

        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        choice = input("Choice? (1-4): ").strip()

        if choice == "1":
            generator.regenerate()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            palette_index = (palette_index + 1) % len(PALETTES)
        elif choice == "4":
            break
        else:
            input("Invalid choice. Press Enter to continue...")
