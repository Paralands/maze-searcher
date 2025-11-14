from typing import Iterator
from maze_searcher.algorithms.maze_solver_algorithm import MazeSolverAlgorithm
import numpy as np

class MazeSolver:
    def __init__(self, grid: np.ndarray, type: MazeSolverAlgorithm) -> None:
        """
        Initializes a MazeSolver object with a specified maze and algorithm type.

        Args:
            grid (np.ndarray): The maze grid to be solved.
            type (MazeSolverAlgorithm): The maze solving algorithm to use.
        
        Returns:
            None
        """
        self.grid = grid
        self.type = type

    def solve(self, start: tuple[int, int], end: tuple[int, int]) -> Iterator[np.ndarray]:
        """
        Solve the maze from start to end coordinates.

        Args:
            start (tuple[int, int]): Starting coordinates.
            end (tuple[int, int]): Ending coordinates.

        Returns:
            Iterator[np.ndarray]: The maze grid at each step of the solving process.
        """    
        if self.type == MazeSolverAlgorithm.ASTAR:
            from .solvers.astar_solver import ASTARSolver
            return ASTARSolver(self.grid, start, end).find_path()
        else:
            raise NotImplementedError(f"Solve method for {self.type} is not implemented yet.")