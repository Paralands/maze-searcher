import pygame
import numpy as np

class Maze():
    def __init__(self, size: int = 100):
        if (size < 50 or size > 500):
            raise ValueError("Maze size should be between 50 and 500 squares") 

        self.maze_size = size
        #TODO: improve block_size to be proportionate to the screen 
        self.block_size_px = 10 
        self.clock = pygame.time.Clock()
    
    def run(self, randomize: bool = False):
        pygame.init()

        self.screen = pygame.display.set_mode((self.maze_size*10, self.maze_size*10))
        self.screen.fill((0, 0, 0))
        if randomize:
            self.randomize()

        self.draw_random_line()

        running = True
        drawing = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                    self._draw_rectangle(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                elif event.type == pygame.MOUSEMOTION and drawing:
                    self._draw_rectangle(event)
                    
            pygame.display.flip()

        pygame.quit()

    def randomize(self):
        fields = np.random.choice([True, False], size=(self.maze_size, self.maze_size))
        
        for (i,j), value in np.ndenumerate(fields):
            if value:
                self._draw_rectangle_at_square(i, j)

    def draw_random_line(self, length: int = 1000):  
        fields = np.zeros((self.maze_size, self.maze_size), dtype=int)
        x = np.random.randint(10, self.maze_size - 10)
        y = np.random.randint(10, self.maze_size - 10)

        fields[x, y] = 1
        self._draw_rectangle_at_square(x, y, 125, 125, 125)

        for n in range(length):
            possible_moves = []
            if (x + 1 < self.maze_size and fields[x + 1, y] == 0 and self._count_field_neighbours(fields, x+1, y) < 2):
                possible_moves.append([x + 1, y])
            if (x - 1 >= 0 and fields[x - 1, y] == 0 and self._count_field_neighbours(fields, x-1, y) < 2):
                possible_moves.append([x - 1, y])
            if (y + 1 < self.maze_size and fields[x, y + 1] == 0 and self._count_field_neighbours(fields, x, y+1) < 2):
                possible_moves.append([x, y + 1])
            if (y - 1 >= 0 and fields[x, y - 1] == 0 and self._count_field_neighbours(fields, x, y-1) < 2):
                possible_moves.append([x, y - 1])

            if not possible_moves:
                break

            next_move = np.random.randint(0, len(possible_moves))
            x, y = possible_moves[next_move]
            self._draw_rectangle_at_square(x, y)
            fields[x, y] = 1

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
        

    def _draw_rectangle(self, event) -> None:
        x, y = event.pos
        pygame.draw.rect(self.screen, 
                         (255,255,255), 
                         ((x // self.block_size_px) * self.block_size_px, 
                          (y // self.block_size_px) * self.block_size_px, 
                          self.block_size_px, 
                          self.block_size_px))
        
    def _draw_rectangle_at_square(self, x, y, r = 255, g = 255, b = 255) -> None:
        pygame.draw.rect(self.screen, 
                         (r,g,b), 
                         (x * self.block_size_px,
                          y * self.block_size_px, 
                          self.block_size_px, 
                          self.block_size_px))
