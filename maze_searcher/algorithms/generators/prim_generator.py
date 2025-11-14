from typing import Iterator
import numpy as np
from .generator_base import GeneratorBase

class PrimGenerator(GeneratorBase):
    """
    Maze generator using Prim's algorithm.
    """

    def __init__(self, maze_size: int):
        """
        Initializes the Prim maze generator.
        Args:
            maze_size (int): Size of the maze (recommended to be odd).
        """
        self.size = maze_size

    def generate(self) -> Iterator[np.ndarray]:
        """
        Generates a maze using Prim's algorithm.

        Yields:
            np.ndarray: The maze grid at each step of generation.
        """
        # 0 = wall, 1 = path
        grid = np.zeros((self.size, self.size), dtype=int)

        # Start from a random cell
        start_x = np.random.randint(1, self.size // 2) * 2 - 1
        start_y = np.random.randint(1, self.size // 2) * 2 - 1
        grid[start_x, start_y] = 1

        frontiers = []

        def add_frontiers(x, y):
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.size - 1 and 0 < ny < self.size - 1 and grid[nx, ny] == 0:
                    frontiers.append((nx, ny, x, y))

        add_frontiers(start_x, start_y)
        yield grid.copy()

        while frontiers:
            # Pick random frontier wall
            f_idx = np.random.randint(0, len(frontiers))
            x, y, px, py = frontiers.pop(f_idx)

            # If cell is not yet part of the maze
            if grid[x, y] == 0:
                grid[x, y] = 1
                # Carve path between parent and this cell
                grid[(x + px) // 2, (y + py) // 2] = 1

                add_frontiers(x, y)

                yield grid.copy()

        yield grid.copy()
