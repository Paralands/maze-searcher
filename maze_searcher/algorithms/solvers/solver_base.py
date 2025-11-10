from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np

class SolverBase(ABC):
    """
    Abstract base class for maze solvers.
    """
    
    @abstractmethod
    def find_path(self) -> Iterator[np.ndarray]:
        """
        Find a path through the maze.

        Yields:
            Iterator[np.ndarray]: The current state of the maze grid at each step.
        """
        pass
    
    @abstractmethod
    def get_solution(self) -> list[tuple[int, int]]:
        """
        Get the final solution path as a list of coordinates.

        Returns:
            list[tuple[int, int]]: The list of coordinates representing the solution path.
        """
        pass
        