from typing import Iterator
import numpy as np

from .solver_base import SolverBase

class ASTARSolver(SolverBase):
    def __init__(self, maze_size: int):
        self.size = maze_size

    def find_path(self) -> Iterator[np.ndarray]:
        pass
            
                
        