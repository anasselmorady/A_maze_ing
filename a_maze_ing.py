from __future__ import annotations

import sys

from config_parser import parse_config
from mazegen.maze import Maze
from mazegen.pattern import apply_42_pattern
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver
from writer import write_output
from display import interactive_menu


def main() -> None:
    """Program entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit()

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
        sys.exit()
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit()
    except KeyboardInterrupt:
        print("\nGoodbye.")
        sys.exit()
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit()


if __name__ == "__main__":
    main()
