from typing import Iterator
import numpy as np

from .generator_base import GeneratorBase

class PRIMGenerator(GeneratorBase):
    def __init__(self, maze_size: int):
        self.size = maze_size

    def generate(self) -> Iterator[np.ndarray]:
        pass
            
                
        