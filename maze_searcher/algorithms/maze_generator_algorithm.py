from enum import Enum, auto

class MazeGeneratorAlgorithm(Enum):
    """
    Enumeration of maze generation algorithms.
    """
    DFS = auto()
    PRIM = auto()
    KRUSKAL = auto()
    RANDOM_LINES = auto()
