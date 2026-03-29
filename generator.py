from __future__ import annotations

import random

from maze import DIRS, OPPOSITE, Maze
from pattern import apply_42_pattern


class MazeGenerator:
    """Generate maze using DFS."""

    def __init__(self, maze: Maze, seed: int | None = None) -> None:
        self.maze = maze
        self.random = random.Random(seed)

    def _unvisited_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        """Return valid DFS neighbors."""
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

    def _remove_wall(self, x: int, y: int, nx: int, ny: int, direction: str) -> None:
        """Open wall between two adjacent cells."""
        self.maze.grid[y][x].walls[direction] = False
        self.maze.grid[ny][nx].walls[OPPOSITE[direction]] = False

    def generate(self) -> None:
        """Generate maze with iterative DFS."""
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

        while stack:
            x, y = stack[-1]
            neighbors = self._unvisited_neighbors(x, y)

            if not neighbors:
                stack.pop()
                continue

            direction, nx, ny = self.random.choice(neighbors)
            self._remove_wall(x, y, nx, ny, direction)
            self.maze.grid[ny][nx].visited = True
            stack.append((nx, ny))

        if not self.maze.perfect:
            self._add_extra_openings(attempts = max(1, (self.maze.width * self.maze.height) // 10))

    def regenerate(self) -> None:
        """Generate a new maze."""
        self.random.seed(self.random.randint(0, 10**9))
        self.generate()

    def _add_extra_openings(self, attempts: int = 10) -> None:
        """Open extra walls to create loops when PERFECT is False."""
        for _ in range(attempts):
            x = self.random.randint(0, self.maze.width - 1)
            y = self.random.randint(0, self.maze.height - 1)

            if self.maze.grid[y][x].blocked:
                continue

            candidates: list[tuple[str, int, int]] = []

            for direction, (dx, dy) in DIRS.items():
                nx = x + dx
                ny = y + dy

                if not self.maze.in_bounds(nx, ny):
                    continue
                if self.maze.grid[ny][nx].blocked:
                    continue

                candidates.append((direction, nx, ny))

            if not candidates:
                continue

            direction, nx, ny = self.random.choice(candidates)

            if self.maze.grid[y][x].walls[direction]:
                self._remove_wall(x, y, nx, ny, direction)
1111111