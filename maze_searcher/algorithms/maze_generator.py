from collections.abc import Iterator
import numpy as np

from .maze_generator_algorithm import MazeGeneratorAlgorithm

class MazeGenerator():
    """
    MazeGenerator class responsible for generating mazes using different algorithms.
    """

    def __init__(self, size: int, type: MazeGeneratorAlgorithm = MazeGeneratorAlgorithm.DFS):
        """
        Initializes a MazeGenerator object with a specified size and algorithm type.
        
        Args:
            size (int): Size of the maze to be generated.
            type (MazeGeneratorAlgorithm): The maze generation algorithm to use (default is DFS).

        Returns:
            None
        """
        self.size = size
        self.type = type

    def generate(self) -> Iterator[np.ndarray]:
        """
        Generates the maze using the specified algorithm provided during initialization.
        
        Returns:
            An iterator that yields the maze grid at each step of generation.
        """
        if(self.type == MazeGeneratorAlgorithm.DFS):
              from .generators import DFSGenerator
              return DFSGenerator(maze_size=self.size).generate()