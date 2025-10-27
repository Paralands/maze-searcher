import queue
import pygame
import numpy as np
import asyncio
import time

from .maze_generator import MazeGenerator
from .maze_generator_algorithm import MazeGeneratorAlgorithm

#TODO: catch exceptions in maze running and generating like stack overflow etc.

class Maze():
    def __init__(self, size: int = 100):
        if (size < 50 or size > 500):
            raise ValueError("Maze size should be between 50 and 500 squares") 

        self.maze_size = size

        #TODO: improve block_size to be proportionate to the screen size
        self.block_size_px = 20 

        # Queues for thread-safe drawing
        self.draw_queue = queue.Queue()

        self.grid = np.zeros((self.maze_size, self.maze_size), dtype=int)  # 0 = wall, 1 = path
        
    #TODO: make the show_process functionality work
    def generate(self, type: MazeGeneratorAlgorithm = MazeGeneratorAlgorithm.DFS, show_process: bool = False, by_space_bar: bool = False, delay_ms: int = 10) -> None:
        print(f"Generating maze using {type.name} algorithm...")
        self.generator = MazeGenerator(size=self.maze_size, type=type)

        if show_process:
            self._show_generation_process(self.generator, by_space_bar, delay_ms)
        else:
            grid = self.generator.generate()
            for grid in grid:
                final_grid = grid
            if final_grid is not None:
                self.set_grid(final_grid)

    def randomize(self, strict = True):
        if strict:
            self.randomize_strict()
        else: self.randomize_relaxed

    def randomize_strict(self, amount = 50):
        fields = np.zeros((self.maze_size, self.maze_size), dtype=int)

        for n in range(amount):
            fields = self.draw_random_line(fields)

    def randomize_relaxed(self):
        fields = np.random.choice([True, False], size=(self.maze_size, self.maze_size))

        for (i,j), value in np.ndenumerate(fields):
            if value:
                self.draw_rectangle_at_square(i, j)

    def draw_random_line(self, fields: np.ndarray | None = None, length: int = 1000): 
        if fields is None:
            fields = np.zeros((self.maze_size, self.maze_size), dtype=int)

        x = np.random.randint(0, self.maze_size)
        y = np.random.randint(0, self.maze_size)

        fields[x, y] = 1
        self.draw_rectangle_at_square(x, y, 255, 255, 255)

        for n in range(length):
            possible_moves = self._get_possible_moves(fields, x, y)

            if not possible_moves:
                possible_moves = self._get_possible_moves(fields, x, y, max_neighbours=2)

            if not possible_moves:
                possible_moves = self._get_possible_moves(fields, x, y, max_neighbours=3)

            if not possible_moves:
                break

            next_move = np.random.randint(0, len(possible_moves))
            x, y = possible_moves[next_move]
            self.draw_rectangle_at_square(x, y)
            #TODO: delay to visualize the process of setting the grid
            fields[x, y] = 1
        
        return fields
    
    def size(self) -> int:
        return self.maze_size
    
    def set_grid(self, grid: list[list[int]] | np.ndarray, show_process: bool = False) -> None:
        # 0 = wall, 1 = path
        grid = np.array(grid)
        self.grid = grid

        for (x, y), value in np.ndenumerate(grid):
            if value == 0:
                self.draw_rectangle_at_square(x, y, 255, 255, 255)
                #TODO: save the grid in self.grid
                #if (show_process):
                    #TODO: delay to visualize the process of setting the grid
                    
        return

    #TODO: fix the show_process functionality
    def _show_generation_process(self, generator: MazeGenerator, by_space_bar: bool = False, delay_ms: int = 10) -> None:
        if by_space_bar is None and delay_ms is None:
            raise ValueError("Either by_space_bar or delay_ms must be provided")
        
        if not self.generator:
            return 
        
        for grid in generator.generate():
            self.set_grid(grid)         
            pygame.time.wait(delay_ms)

    def _count_field_neighbours(self, fields, x, y) -> int:
        count = 0

        if (x + 1 < len(fields) and fields[x + 1, y] == 1):
            count += 1
        if (x - 1 >= 0 and fields[x - 1, y] == 1):
            count += 1
        if (y + 1 < len(fields) and fields[x, y + 1] == 1):
            count += 1
        if (y - 1 >= 0 and fields[x, y - 1] == 1):
            count += 1

        return count
    
    def _get_possible_moves(self, fields, x, y, max_neighbours=1) -> list[list[int]]:
        possible_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if (
                0 <= nx < self.maze_size
                and 0 <= ny < self.maze_size
                and fields[nx, ny] == 0
                and self._count_field_neighbours(fields, nx, ny) <= max_neighbours
            ): 
                possible_moves.append([nx, ny])

        return possible_moves
        
    def draw_rectangle(self, event, r: int = 255, g: int = 255, b: int = 255) -> None:
        if not 0 <= r <= 255 or not 0 <= g <= 255 or not 0 <= b <= 255:
            raise ValueError("Parametrs r, g, b must be in range of (0, 256)")

        x, y = event.pos
        self.draw_queue.put((x // self.block_size_px, y // self.block_size_px, (r, g, b)))  
        self.grid[x // self.block_size_px, y // self.block_size_px] = 1
        
    def draw_rectangle_at_square(self, x: int, y: int, r: int = 255, g: int = 255, b: int = 255) -> None:
        if not 0 <= r <= 255 or not 0 <= g <= 255 or not 0 <= b <= 255:
            raise ValueError("Parametrs r, g, b must be in range of (0, 256)")
            
        if not (0 <= x < self.maze_size and 0 <= y < self.maze_size):
            raise ValueError("Parametrs x and y must be in range of the maze size")
        
        self.draw_queue.put((x, y, (r, g, b)))  
        self.grid[x,y]=1   
        
    def erase_rectangle(self, event) -> None:
        self.draw_rectangle(event, 0, 0, 0)