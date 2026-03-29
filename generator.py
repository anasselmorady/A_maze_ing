from __future__ import annotations

import random
import time

from maze import DIRS, OPPOSITE, Maze
from pattern import apply_42_pattern


class MazeGenerator:
    """Generate maze using DFS."""

    def __init__(self, maze: Maze, seed: int | None = None) -> None:
        self.maze = maze
        self.random = random.Random(seed)

    def _unvisited_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        neighbors: list[tuple[str, int, int]] = []

        for direction, (dx, dy) in DIRS.items():
            nx = x + dx
            ny = y + dy

            if not self.maze.in_bounds(nx, ny):
                continue
            if self.maze.grid[ny][nx].visited:
                continue
            if self.maze.grid[ny][nx].blocked:
                continue

            neighbors.append((direction, nx, ny))

        return neighbors

    def _valid_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        neighbors: list[tuple[str, int, int]] = []

        for direction, (dx, dy) in DIRS.items():
            nx = x + dx
            ny = y + dy

            if not self.maze.in_bounds(nx, ny):
                continue
            if self.maze.grid[ny][nx].blocked:
                continue

            neighbors.append((direction, nx, ny))

        return neighbors

    def _remove_wall(self, x: int, y: int, nx: int, ny: int, direction: str) -> None:
        self.maze.grid[y][x].walls[direction] = False
        self.maze.grid[ny][nx].walls[OPPOSITE[direction]] = False

    def _add_extra_openings(self, attempts: int = 10) -> None:
        for _ in range(attempts):
            x = self.random.randint(0, self.maze.width - 1)
            y = self.random.randint(0, self.maze.height - 1)

            if self.maze.grid[y][x].blocked:
                continue

            neighbors = self._valid_neighbors(x, y)
            if not neighbors:
                continue

            direction, nx, ny = self.random.choice(neighbors)

            if self.maze.grid[y][x].walls[direction]:
                self._remove_wall(x, y, nx, ny, direction)

    def generate(
        self,
        animate: bool = False,
        frame_callback=None,
        delay: float = 0.02,
    ) -> None:
        """Generate maze with iterative DFS.

        animate=True will call frame_callback(maze, current_cell) each step.
        """
        self.maze.reset()
        apply_42_pattern(self.maze)

        start_x, start_y = self.maze.entry
        exit_x, exit_y = self.maze.exit

        if self.maze.grid[start_y][start_x].blocked:
            raise ValueError("ENTRY cannot be inside 42 pattern.")
        if self.maze.grid[exit_y][exit_x].blocked:
            raise ValueError("EXIT cannot be inside 42 pattern.")

        self.maze.grid[start_y][start_x].visited = True
        stack: list[tuple[int, int]] = [(start_x, start_y)]

        if animate and frame_callback is not None:
            frame_callback(self.maze, (start_x, start_y))
            time.sleep(delay)

        while stack:
            x, y = stack[-1]
            neighbors = self._unvisited_neighbors(x, y)

            if not neighbors:
                stack.pop()
                if animate and frame_callback is not None:
                    current = stack[-1] if stack else None
                    frame_callback(self.maze, current)
                    time.sleep(delay)
                continue

            direction, nx, ny = self.random.choice(neighbors)
            self._remove_wall(x, y, nx, ny, direction)
            self.maze.grid[ny][nx].visited = True
            stack.append((nx, ny))

            if animate and frame_callback is not None:
                frame_callback(self.maze, (nx, ny))
                time.sleep(delay)

        if not self.maze.perfect:
            attempts = max(10, (self.maze.width * self.maze.height) // 3)
            self._add_extra_openings(attempts)

    def regenerate(self) -> None:
        self.random.seed(self.random.randint(0, 10**9))
        self.generate()
