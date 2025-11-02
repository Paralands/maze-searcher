from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np

class GeneratorBase(ABC):
    def generate(self) -> Iterator[np.ndarray]:
        pass

        