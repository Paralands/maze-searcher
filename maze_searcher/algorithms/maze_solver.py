from typing import Iterator

import numpy as np


class MazeSolver:
    def __init__(self, maze):
        self.maze = maze

    def solve(self, start: tuple[int, int], end: tuple[int, int]) -> Iterator[np.ndarray]:
        """
        Solve the maze from start to end coordinates.

        Args:
            start (tuple[int, int]): Starting coordinates.
            end (tuple[int, int]): Ending coordinates.

        Returns:
            Iterator[np.ndarray]: The maze grid at each step of the solving process.
        """
        
        from .solvers.astar_solver import ASTARSolver
        return ASTARSolver(self.maze, start, end).find_path()