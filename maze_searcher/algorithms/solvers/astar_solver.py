from typing import Iterator
import heapq
import numpy as np

from maze_searcher.maze import Maze

from .solver_base import SolverBase

class ASTARSolver(SolverBase):
    """
    Maze solver using the A* algorithm.
    """

    def __init__(self, maze: Maze, start: tuple[int, int], end: tuple[int, int]):
        """
        Initialize the A* maze solver.

        Args:
            maze (Maze): The maze to solve.
            start (tuple[int, int]): The starting coordinates in the maze.
            end (tuple[int, int]): The ending coordinates in the maze.
        """
        self.maze = maze
        self.start = start
        self.end = end
        self.rows, self.cols = maze.grid.shape

    def heuristic(self, a: tuple[int, int], b: tuple[int, int]) -> int:
        """
        Calculate the Manhattan distance heuristic between two points.
        
        Args:
            a (tuple[int, int]): First point coordinates.
            b (tuple[int, int]): Second point coordinates.
        Returns:

            int: The Manhattan distance between points a and b.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node: tuple[int, int]) -> Iterator[tuple[int, int]]:
        """
        Get valid neighboring nodes.

        Args:
            node (tuple[int, int]): Current node coordinates.

        Yields:
            tuple[int, int]: Valid neighboring coordinates.
        """
        r, c = node
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.maze.grid[nr, nc] != 0:  # not a wall
                    yield (nr, nc)
    
    def find_path(self) -> Iterator[np.ndarray]:
        """
        Find a path through the maze using the A* algorithm.

        Yields:
            Iterator[np.ndarray]: The current state of the maze grid at each step.
        """
        open_set = []
        heapq.heappush(open_set, (self.heuristic(self.start, self.end), 0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        visited = set()

        grid = self.maze.grid.copy()

        while open_set:
            _, current_g, current = heapq.heappop(open_set)

            # goal reached
            if current == self.end:
                node = current
                while node != self.start:
                    r, c = node
                    if grid[r, c] not in (3, 4):
                        grid[r, c] = 5  # solution color
                    node = came_from[node]
                    yield grid.copy()
                return

            if current in visited:
                continue
            visited.add(current)

            r, c = current
            if grid[r, c] not in (3, 4):
                grid[r, c] = 2  # mark visited
            yield grid.copy()

            for neighbor in self.neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, self.end)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                    came_from[neighbor] = current

    def get_solution(self) -> list[tuple[int, int]]:
        """
        Compute and return the final solution path using the A* algorithm.

        Returns:
            list[tuple[int, int]]: Ordered list of coordinates from start to end.
        """
        open_set = []
        heapq.heappush(open_set, (self.heuristic(self.start, self.end), 0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        visited = set()

        while open_set:
            _, current_g, current = heapq.heappop(open_set)

            if current == self.end:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start)
                path.reverse()
                return path

            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.neighbors(current):
                tentative_g = current_g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, self.end)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                    came_from[neighbor] = current

        # No path found
        return []
