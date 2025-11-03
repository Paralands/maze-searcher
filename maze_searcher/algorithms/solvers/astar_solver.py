from typing import Iterator
import numpy as np

from maze_searcher.maze import Maze

from .solver_base import SolverBase

class ASTARSolver(SolverBase):
    """
    Maze solver using the A* algorithm.
    """

    def __init__(self, maze: Maze):
        """
        Initialize the A* maze solver.

        Args:
            maze (Maze): The maze to solve.
        """
        self.maze = maze

    def find_path(self) -> Iterator[np.ndarray]:
        """
        Find a path through the maze.

        Yields:
            Iterator[np.ndarray]: The current state of the maze grid at each step.
        """
        pass
            
                
        