from maze_generator_algorithm import MazeGeneratorAlgorithm

class MazeGenerator():
    def __init__(self, size: int, type: MazeGeneratorAlgorithm = MazeGeneratorAlgorithm.DFS):
        self.size = size
        self.type = type

    def generate(self) -> None:
        if(self.type == MazeGeneratorAlgorithm.DFS):
              from algorithms import DFSGenerator
              return DFSGenerator(size=self.size).generate()