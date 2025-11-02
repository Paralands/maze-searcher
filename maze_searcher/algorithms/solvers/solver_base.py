from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np

class SolverBase(ABC):
    def find_path(self) -> Iterator[np.ndarray]:
        pass

        