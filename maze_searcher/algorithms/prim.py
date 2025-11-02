from typing import Iterator
import numpy as np

from .generator_base import GeneratorBase

class PRIMGenerator(GeneratorBase):
    def __init__(self, maze_size: int):
        self.size = maze_size

    def generate(self) -> Iterator[np.ndarray]:
        # Initialize grid of walls
        # 0 = wall, 1 = path
        grid = np.zeros((self.size, self.size), dtype=int)

        visited = []

        # Start at a random odd cell (representing the path-cell)
        start = (np.random.randint(2, self.size // 2) * 2 - 1, np.random.randint(2, self.size // 2) * 2 - 1)
        visited.append(start) 
        grid[start] = 1 
        
        # Initial yield of the starting grid
        yield grid.copy()

        # Jumps two to account for walls
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        
        