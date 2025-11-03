from typing import Iterator
import numpy as np

from .generator_base import GeneratorBase

class PRIMGenerator(GeneratorBase):
    """
    Maze generator using Prim's algorithm.
    """

    def __init__(self, maze_size: int):
        """
        Initialize the Prim maze generator.

        Args:
            maze_size (int): Size of the maze (recommended to be odd).
        """
        super().__init__(maze_size)

    def generate(self) -> Iterator[np.ndarray]:
        """
        Generate a maze using Prim's algorithm.

        Yields:
            Iterator[np.ndarray]: The current state of the maze grid at each step.
        """

        pass
            
                
        