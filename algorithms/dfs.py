import numpy as np


class DFSGenerator():
    def __init__(self, size: int):
        self.size = size

    def generate(self) -> list[list[int]]:
        # Initialize grid: 0 = wall, 1 = path
        grid = np.zeros((self.size, self.size), dtype=int)

        stack = []

        # Start at a random even cell (representing the path-cell)
        start = (np.random.randint(1, self.size // 2) * 2, np.random.randint(1, self.size // 2) * 2)
        stack.append(start) 
        grid[start] = 1 

        # Jumps two to account for walls
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]

        while stack:
            cell = stack[-1]
            neighbours = []

            # Check all neighbourds
            for dx, dy in directions:
                nx, ny = cell[0] + dx, cell[1] + dy
                if (0 <= nx < self.size and 0 <= ny < self.size and grid[nx, ny] == 0):
                    neighbours.append((nx, ny))

            if neighbours:
                neighbour = neighbours[np.random.randint(0, len(neighbours))]
                stack.append(neighbour)

                # Carve path between current and neighbor
                nx, ny = neighbour[0], neighbour[1]
                wall_x, wall_y = (nx + cell[0]) // 2, (ny + cell[1]) // 2
                grid[neighbour] = 1      
                grid[wall_x, wall_y] = 1
            else:
                stack.pop()
                
        return grid

        