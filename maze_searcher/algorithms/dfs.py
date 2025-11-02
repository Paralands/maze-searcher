from typing import Iterator
import numpy as np


class DFSGenerator():
    def __init__(self, size: int):
        self.size = size

    def generate(self) -> Iterator[np.ndarray]:
        # Initialize grid of walls
        # 0 = wall, 1 = path
        grid = np.zeros((self.size, self.size), dtype=int)

        stack = []

        # Start at a random odd cell (representing the path-cell)
        start = (np.random.randint(2, self.size // 2) * 2 - 1, np.random.randint(2, self.size // 2) * 2 - 1)
        stack.append(start) 
        grid[start] = 1 
        
        # Initial yield of the starting grid
        yield grid.copy()

        # Jumps two to account for walls
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]

        while stack:
            cell = stack[-1]
            neighbours = []

            # Check all neighbourds
            for dx, dy in directions:
                nx, ny = cell[0] + dx, cell[1] + dy

                # If neighbour is within bounds and is a wall
                if (0 < nx < self.size and 0 < ny < self.size and grid[nx, ny] == 0):
                    neighbours.append((nx, ny))

            if neighbours:
                neighbour = neighbours[np.random.randint(0, len(neighbours))]
                stack.append(neighbour)

                # Carve path between current and neighbor
                nx, ny = neighbour[0], neighbour[1]
                path_x, path_y = (nx + cell[0]) // 2, (ny + cell[1]) // 2
                grid[neighbour] = 1      
                grid[path_x, path_y] = 1

                # Yield the current state of the grid
                yield grid.copy()
            else:
                stack.pop()

        