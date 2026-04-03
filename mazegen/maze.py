from __future__ import annotations


DIRS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

OPPOSITE = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E",
}


class Cell:
    """One maze cell."""

    def __init__(self) -> None:
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }
        self.visited = False
        self.blocked = False


class Maze:
    """Maze structure and shared helpers."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.perfect = perfect
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self._validate()

    def _validate(self) -> None:
        """Validate maze settings."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("WIDTH and HEIGHT must be greater than 0.")

        ex, ey = self.entry
        xx, xy = self.exit

        if not self.in_bounds(ex, ey):
            raise ValueError("ENTRY is outside maze bounds.")
        if not self.in_bounds(xx, xy):
            raise ValueError("EXIT is outside maze bounds.")
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different.")

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are inside maze."""
        return 0 <= x < self.width and 0 <= y < self.height

    def reset(self) -> None:
        """Reset all cells."""
        self.grid = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]
