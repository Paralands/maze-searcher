class MazeSolver:
    def __init__(self, maze):
        self.maze = maze

    def solve(self, start, end):
        raise NotImplementedError("This method should be overridden by subclasses")