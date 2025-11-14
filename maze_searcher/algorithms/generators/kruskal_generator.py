from typing import Iterator
import numpy as np
from .generator_base import GeneratorBase

class KruskalGenerator(GeneratorBase):
    """
    Maze generator using Kruskal's algorithm.
    """

    def __init__(self, maze_size: int):
        """
        Initializes the Kruskal maze generator.
        Args:
            maze_size (int): Size of the maze (recommended to be odd).
        """
        self.size = maze_size

    def generate(self) -> Iterator[np.ndarray]:
        """
        Generates a maze using Kruskal's algorithm.

        Yields:
            np.ndarray: The maze grid at each step of generation.
        """
        size = self.size
        grid = np.zeros((size, size), dtype=int)

        # Initialize all cells as separate sets
        sets = {}
        for x in range(1, size, 2):
            for y in range(1, size, 2):
                grid[x, y] = 1
                sets[(x, y)] = (x, y)  # representative parent for union-find

        # Helper functions for union-find
        def find(cell):
            path = []
            while sets[cell] != cell:
                path.append(cell)
                cell = sets[cell]
            for c in path:
                sets[c] = cell
            return cell

        def union(a, b):
            ra, rb = find(a), find(b)
            sets[rb] = ra

        # List all walls between cells
        walls = []
        for x in range(1, size, 2):
            for y in range(1, size, 2):
                if x < size - 2:
                    walls.append(((x + 1, y), (x, y), (x + 2, y)))  # wall, cell1, cell2
                if y < size - 2:
                    walls.append(((x, y + 1), (x, y), (x, y + 2)))

        np.random.shuffle(walls)

        for wall, cell1, cell2 in walls:
            if find(cell1) != find(cell2):
                # Remove wall
                wx, wy = wall
                grid[wx, wy] = 1
                union(cell1, cell2)
                yield grid.copy()

        yield grid.copy()
