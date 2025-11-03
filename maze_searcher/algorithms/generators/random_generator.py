from typing import Iterator

import numpy as np
from maze_searcher.algorithms.maze_generator import MazeGenerator


class RandomMazeGenerator(MazeGenerator):

    def __init__(self, maze_size: int):
        """
        Initialize the Random Lines maze generator.

        Args:
            maze_size (int): Size of the maze (recommended to be odd).
        """
        super().__init__(maze_size)

    def generate(self) -> Iterator[np.ndarray]:
        """
        Generate a maze using Random Lines algorithm.

        Yields:
            Iterator[np.ndarray]: The current state of the maze grid at each step.
        """

        pass