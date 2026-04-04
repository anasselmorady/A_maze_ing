from __future__ import annotations

from collections import deque

from mazegen.maze import DIRS, Maze
import sys


class MazeSolver:
    """Solve maze using BFS."""

    def __init__(self, maze: Maze) -> None:
        try:
            if not isinstance(maze, Maze):
                raise TypeError("maze must be an instance of Maze.")

        except Exception as e:
            print(e)
            sys.exit()
        self.maze = maze

    def shortest_path(self) -> str:
        """Return shortest path from entry to exit."""
        queue: deque[tuple[int, int]] = deque([self.maze.entry])
        parents: dict[tuple[int, int], tuple[int, int] | None] = {
            self.maze.entry: None
        }
        move_used: dict[tuple[int, int], str] = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.maze.exit:
                break

            for direction, (dx, dy) in DIRS.items():
                if self.maze.grid[y][x].walls[direction]:
                    continue

                nx = x + dx
                ny = y + dy

                if not self.maze.in_bounds(nx, ny):
                    continue
                if self.maze.grid[ny][nx].blocked:
                    continue
                if (nx, ny) in parents:
                    continue

                parents[(nx, ny)] = (x, y)
                move_used[(nx, ny)] = direction
                queue.append((nx, ny))

        if self.maze.exit not in parents:
            raise ValueError("No valid path from ENTRY to EXIT.")

        path: list[str] = []
        current = self.maze.exit

        while current != self.maze.entry:
            path.append(move_used[current])
            parent = parents[current]
            if parent is None:
                break
            current = parent

        path.reverse()
        return "".join(path)
