import pygame
import numpy as np

from maze_generator import MazeGenerator
from maze_generator_algorithm import MazeGeneratorAlgorithm

class Maze():
    def __init__(self, size: int = 100):
        if (size < 50 or size > 500):
            raise ValueError("Maze size should be between 50 and 500 squares") 

        self.maze_size = size
        #TODO: improve block_size to be proportionate to the screen 
        self.block_size_px = 20 
        self.clock = pygame.time.Clock()
    
    def run(self, randomize: bool = False):
        pygame.init()

        self.screen = pygame.display.set_mode((self.maze_size*10, self.maze_size*10))
        self.screen.fill((0, 0, 0))
        if randomize:
            self.randomize()

        generator = MazeGenerator(size=self.maze_size, type=MazeGeneratorAlgorithm.DFS)
        grid = generator.generate()
        self.set_grid(grid, True)

        running = True
        drawing = False
        erasing = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        drawing = True
                        erasing = False
                        self._draw_rectangle(event)
                    elif event.button == 3:
                        drawing = False
                        erasing = True
                        self._erase_rectangle(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                    erasing = False
                elif event.type == pygame.MOUSEMOTION:
                    if drawing:
                        self._draw_rectangle(event)
                    if erasing:
                        self._erase_rectangle(event)
                    
            pygame.display.flip()

        pygame.quit()

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
                self._draw_rectangle_at_square(i, j)

    def draw_random_line(self, fields: np.ndarray | None = None, length: int = 1000): 
        if fields is None:
            fields = np.zeros((self.maze_size, self.maze_size), dtype=int)

        x = np.random.randint(0, self.maze_size)
        y = np.random.randint(0, self.maze_size)

        fields[x, y] = 1
        self._draw_rectangle_at_square(x, y, 255, 255, 255)

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
            self._draw_rectangle_at_square(x, y)
            pygame.time.wait(2)
            pygame.display.flip()
            fields[x, y] = 1
        
        return fields
    
    def size(self) -> int:
        return self.maze_size
    
    def set_grid(self, grid: list[list[int]], show_process: bool = False) -> None:
        # 0 = wall, 1 = path
        for (x, y), value in np.ndenumerate(grid):
            if value == 0:
                self._draw_rectangle_at_square(x, y, 255, 255, 255)
                if (show_process):
                    pygame.display.flip()
        
        pygame.display.flip()
                

    def _count_field_neighbours(self, fields, x, y) -> int:
        count = 0
        if (x + 1 < len(fields) and fields[x + 1, y] == 1):
            count += 1
        if (x - 1 >= 0 and fields[x - 1, y] == 1):
            count += 1
        if (y + 1 < len(fields) and fields[x, y + 1] == 1):
            count += 1      
        if (y - 1 >= 0 and fields[x , y - 1] == 1):
            count += 1
        return count
    
    def _get_possible_moves(self, fields, x, y, max_neighbours = 1) -> list[list[int]]:
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
        

    def _draw_rectangle(self, event, r: int = 255, g: int = 255, b: int = 255) -> None:
        if not 0 <= r <= 255 or not 0 <= g <= 255 or not 0 <= b <= 255:
            raise ValueError("Parametrs r, g, b must be in range of (0, 256)")

        x, y = event.pos
        pygame.draw.rect(self.screen, 
                         (r,g,b), 
                         ((x // self.block_size_px) * self.block_size_px, 
                          (y // self.block_size_px) * self.block_size_px, 
                          self.block_size_px, 
                          self.block_size_px))
        
    def _draw_rectangle_at_square(self, x: int, y: int, r: int = 255, g: int = 255, b: int = 255) -> None:
        if not 0 <= r <= 255 or not 0 <= g <= 255 or not 0 <= b <= 255:
            raise ValueError("Parametrs r, g, b must be in range of (0, 256)")
            
        # TODO: Check x and y value to be in range
        
        pygame.draw.rect(self.screen, 
                         (r,g,b), 
                         (x * self.block_size_px,
                          y * self.block_size_px, 
                          self.block_size_px, 
                          self.block_size_px))
        
    def _erase_rectangle(self, event) -> None:
        self._draw_rectangle(event, 0, 0, 0)