from typing import Iterator
import numpy as np
import random
from maze_searcher.algorithms.maze_generator import MazeGenerator


class RandomLinesGenerator(MazeGenerator):
    def __init__(self, maze_size: int):
        """
        Initialize the Random Lines maze generator.

        Args:
            maze_size (int): Size of the maze (recommended to be odd).
        """
        self.maze_size = maze_size
        self.fields = np.zeros((maze_size, maze_size), dtype=int)

    def generate(self) -> Iterator[np.ndarray]:
        """
        Generate a maze using a simple random walk algorithm.
        
        Yields:
            np.ndarray: The maze grid at each step of generation.
        """
        fields = np.zeros((self.maze_size, self.maze_size), dtype=int)

        # Start from a random odd cell
        x, y = random.randrange(1, self.maze_size, 2), random.randrange(1, self.maze_size, 2)
        fields[x, y] = 1
        yield fields.copy()  # initial step

        stack = [(x, y)]

        while stack:
            x, y = stack[-1]
            possible_moves = self._get_possible_moves(fields, x, y)

            if possible_moves:
                nx, ny = random.choice(possible_moves)
                fields[nx, ny] = 1
                stack.append((nx, ny))
            else:
                stack.pop()

            # yield current maze state at each step
            yield fields.copy()

        self.fields = fields

    def _count_field_neighbours(self, fields, x, y) -> int:
        count = 0
        if x + 1 < len(fields) and fields[x + 1, y] == 1:
            count += 1
        if x - 1 >= 0 and fields[x - 1, y] == 1:
            count += 1
        if y + 1 < len(fields) and fields[x, y + 1] == 1:
            count += 1
        if y - 1 >= 0 and fields[x, y - 1] == 1:
            count += 1
        return count

    def _get_possible_moves(self, fields, x, y, max_neighbours=1) -> list[list[int]]:
        possible_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.maze_size
                and 0 <= ny < self.maze_size
                and fields[nx, ny] == 0
                and self._count_field_neighbours(fields, nx, ny) <= max_neighbours
            ):
                possible_moves.append([nx, ny])
        return possible_moves
