from __future__ import annotations

import random
import time
from typing import Callable, Optional

from mazegen.maze import DIRS, OPPOSITE, Maze
from mazegen.pattern import apply_42_pattern


class MazeGenerator:
    """Generate maze using DFS."""

    def __init__(self, maze: Maze, seed: int | None = None) -> None:
        self._validate_init_inputs(maze, seed)
        self.maze = maze
        self.random = random.Random(seed)

    def _validate_init_inputs(self, maze: Maze, seed: int | None) -> None:
        """Validate constructor inputs."""
        if not isinstance(maze, Maze):
            raise TypeError("maze must be an instance of Maze.")

        if seed is not None and not isinstance(seed, int):
            raise TypeError("seed must be an integer or None.")

    def _validate_generate_inputs(
        self,
        animate: bool,
        frame_callback: Optional[Callable[[Maze, Optional[tuple[int, int]]], None]],
        delay: float,
    ) -> None:
        """Validate generate() inputs."""
        if not isinstance(animate, bool):
            raise TypeError("animate must be True or False.")

        if frame_callback is not None and not callable(frame_callback):
            raise TypeError("frame_callback must be callable or None.")

        if not isinstance(delay, (int, float)):
            raise TypeError("delay must be a number.")

        if delay < 0:
            raise ValueError("delay must be greater than or equal to 0.")

    def _validate_start_end_cells(self) -> None:
        """Validate entry and exit after applying the 42 pattern."""
        start_x, start_y = self.maze.entry
        exit_x, exit_y = self.maze.exit

        if self.maze.grid[start_y][start_x].blocked:
            raise ValueError("ENTRY cannot be inside 42 pattern.")

        if self.maze.grid[exit_y][exit_x].blocked:
            raise ValueError("EXIT cannot be inside 42 pattern.")

    def _unvisited_neighbors(
        self,
        x: int,
        y: int
    ) -> list[tuple[str, int, int]]:
        """Return all valid unvisited neighbors."""
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
        """Return all valid non-blocked neighbors."""
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

    def _remove_wall(
        self,
        x: int,
        y: int,
        nx: int,
        ny: int,
        direction: str
    ) -> None:
        """Open the wall between two adjacent cells."""
        self.maze.grid[y][x].walls[direction] = False
        self.maze.grid[ny][nx].walls[OPPOSITE[direction]] = False

    def _add_extra_openings(self) -> None:
        """Force creation of loops when PERFECT=False."""
        attempts = max(1, (self.maze.width * self.maze.height) // 2)

        for _ in range(attempts):
            x = self.random.randint(0, self.maze.width - 1)
            y = self.random.randint(0, self.maze.height - 1)

            if self.maze.grid[y][x].blocked:
                continue

            closed_neighbors: list[tuple[str, int, int]] = []

            for direction, (dx, dy) in DIRS.items():
                nx = x + dx
                ny = y + dy

                if not self.maze.in_bounds(nx, ny):
                    continue
                if self.maze.grid[ny][nx].blocked:
                    continue

                if self.maze.grid[y][x].walls[direction]:
                    closed_neighbors.append((direction, nx, ny))

            if not closed_neighbors:
                continue

            direction, nx, ny = self.random.choice(closed_neighbors)
            self._remove_wall(x, y, nx, ny, direction)

    def generate(
        self,
        animate: bool = False,
        frame_callback: Optional[
            Callable[[Maze, Optional[tuple[int, int]]], None]
        ] = None,
        delay: float = 0.02,
    ) -> None:
        """Generate maze with iterative DFS."""
        self._validate_generate_inputs(animate, frame_callback, delay)

        self.maze.reset()
        apply_42_pattern(self.maze)
        self._validate_start_end_cells()

        start_x, start_y = self.maze.entry
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
            self._add_extra_openings()

    def regenerate(self) -> None:
        """Generate a new random maze."""
        self.random.seed(self.random.randint(0, 10**9))
        self.generate()