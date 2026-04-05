import sys
import random
from mazegen.maze import DIRS, OPPOSITE, Maze
from mazegen.pattern import apply_42_pattern


class MazeGenerator:
    """Generate maze using DFS."""

    def __init__(self, maze: Maze, seed: int | None = None) -> None:
        """Validate constructor inputs."""
        try:
            if not isinstance(maze, Maze):
                raise TypeError("maze must be an instance of Maze.")

            if seed is not None and not isinstance(seed, int):
                raise TypeError("seed must be an integer or None.")
        except Exception as e:
            print(e)
            sys.exit()

        self.maze = maze
        self.seed = seed

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
        attempts = max(1, (self.maze.width * self.maze.height) // 5)

        for _ in range(attempts):
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)

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

            direction, nx, ny = random.choice(closed_neighbors)
            self._remove_wall(x, y, nx, ny, direction)

    def generate(self) -> None:
        """Generate maze with iterative DFS."""
        if self.seed:
            random.seed(self.seed)

        self.maze.reset()
        apply_42_pattern(self.maze)
        self._validate_start_end_cells()

        start_x, start_y = self.maze.entry
        self.maze.grid[start_y][start_x].visited = True
        stack: list[tuple[int, int]] = [(start_x, start_y)]

        while stack:
            x, y = stack[-1]
            neighbors = self._unvisited_neighbors(x, y)

            if not neighbors:
                stack.pop()
                continue

            direction, nx, ny = random.choice(neighbors)
            self._remove_wall(x, y, nx, ny, direction)
            self.maze.grid[ny][nx].visited = True
            stack.append((nx, ny))

        if not self.maze.perfect:
            self._add_extra_openings()

    def regenerate(self) -> None:
        """Generate a new random maze."""
        self.generate()
