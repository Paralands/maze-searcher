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

        