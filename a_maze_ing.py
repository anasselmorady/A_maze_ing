from __future__ import annotations

import sys

from config_parser import parse_config
from maze import Maze
from pattern import apply_42_pattern
from generator import MazeGenerator
from solver import MazeSolver
from writer import write_output
from display import interactive_menu


def main() -> None:
    """Program entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        config = parse_config(config_file)

        maze = Maze(
            width=config["WIDTH"],
            height=config["HEIGHT"],
            entry=config["ENTRY"],
            exit_=config["EXIT"],
            perfect=config["PERFECT"],
        )

        apply_42_pattern(maze)

        generator = MazeGenerator(maze, seed=config["SEED"])
        generator.generate()

        solver = MazeSolver(maze)
        path = solver.shortest_path()

        write_output(maze, config["OUTPUT_FILE"], path)

        interactive_menu(
            maze=maze,
            generator=generator,
            solver=solver,
            output_file=config["OUTPUT_FILE"],
        )

    except FileNotFoundError:
        print(f"Error: file not found: {config_file}")
        sys.exit(1)
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGoodbye.")
        sys.exit(0)
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
