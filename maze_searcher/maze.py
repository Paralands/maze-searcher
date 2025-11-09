import queue
from typing import Iterator
import pygame
import numpy as np

from .algorithms import MazeGenerator
from .algorithms import MazeGeneratorAlgorithm

#TODO: catch exceptions in maze running and generating like stack overflow etc.

class Maze():
    """
    Maze class representing a maze structure and providing methods to manipulate it.
    0 = wall, 1 = path
    Walls are white, paths are black
    """
    def __init__(self, size: int = 35, block_size_px: int = 20, wall_color: tuple[int, int, int] = (255, 255, 255), path_color: tuple[int, int, int] = (0, 0, 0)):
        """
        Initializes a Maze object with a specified size.
        
        Args:
            size (int): Size of the maze in squares (default is 100)
            block_size_px (int): Size of each block in pixels (default is 20).
            wall_color (tuple[int, int, int]): RGB color of the walls (default is white).
            path_color (tuple[int, int, int]): RGB color of the paths (default is black).
        
        Raises:
            ValueError: If the size is not between 50 and 500 squares.
        """
        if (size < 20 or size > 100):
            raise ValueError("Maze size should be between 20 and 100 squares") 

        self.maze_size = size

        #TODO: improve block_size to be proportionate to the screen size
        self.block_size_px = block_size_px 

        self.wall_color = wall_color
        self.path_color = path_color

        # Queues for thread-safe drawing, contains a list of (x, y, (r, g, b)) tuples
        # [x, y]
        self.draw_queue = queue.Queue()

        # [row, col]
        # 0 = wall, 1 = path
        self.grid = np.zeros((self.maze_size, self.maze_size), dtype=int)  
        
    def generate(self, type: MazeGeneratorAlgorithm = MazeGeneratorAlgorithm.DFS) -> Iterator[np.ndarray]:
        """
        Generates the maze using the specified algorithm.
        
        Args:
            type (MazeGeneratorAlgorithm): The maze generation algorithm to use (default is DFS).

        Returns:
            An iterator that yields the maze grid at each step of generation.
        """
        self.generator = MazeGenerator(size=self.maze_size, type=type)
        grid_generator = self.generator.generate()

        for grid in grid_generator:
            yield grid


    def size(self) -> int:
        return self.maze_size
    
    def set_grid(self, grid: list[list[int]] | np.ndarray, show_process: bool = False) -> None:
        """Sets the maze grid to the provided grid.
        
        Args:
            grid (list[list[int]] | np.ndarray): The grid to set the maze to.
            show_process (bool): If True, visualizes the process of setting the grid (default is False).

        Returns:
            None
        """
        # 0 = wall, 1 = path
        grid = np.array(grid)
        self.grid = grid

        for (row, col), value in np.ndenumerate(grid):
            # Swap to corespond to the pygame [x,y] convention
            x, y = col, row

            rectangle_list_to_draw = []

            if value == 0:
                rectangle_list_to_draw.append((x, y, self.wall_color))
            elif value == 1:
                rectangle_list_to_draw.append((x, y, self.path_color))

            if rectangle_list_to_draw != []:
                self.draw_rectangle_list(rectangle_list_to_draw)
                
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



    def draw_rectangle(self, pos: tuple[int, int], color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Draws a rectangle at the position of pygame's event with the specified color and updates the grid.
        
        Args:
            pos: The pygame position of the event to draw the rectangle.
            r (int): Red component of the color (0-255).
            g (int): Green component of the color (0-255).
            b (int): Blue component of the color (0-255).

        Returns:
            None
        """
        r, g, b = color
        if not 0 <= r <= 255 or not 0 <= g <= 255 or not 0 <= b <= 255:
            raise ValueError("Parametrs r, g, b must be in range of (0, 256)")

        x, y = pos
        row, col = int(y), int(x)

        self.draw_queue.put([(x // self.block_size_px, y // self.block_size_px, (r, g, b))])

        if (r, g, b) == self.path_color:
            self.grid[row//self.block_size_px, col//self.block_size_px] = 1
        elif (r, g, b) == self.wall_color:
            self.grid[row//self.block_size_px, col//self.block_size_px] = 0

    def draw_rectangle_at_square(self, x: int, y: int, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Draws a rectangle at the specified square coordinates with the given color and updates the grid.
        
        Args:
            x (int): X coordinate of the square.
            y (int): Y coordinate of the square.
            r (int): Red component of the color (0-255).
            g (int): Green component of the color (0-255).
            b (int): Blue component of the color (0-255).
        
        Returns:
            None
        """

        self.draw_rectangle_list([(x, y, color)])

    def draw_rectangle_list(self, rectangles: list[tuple[int, int, tuple[int, int, int]]]) -> None:
        """
        Draws multiple rectangles based on the provided list of rectangle specifications.
        
        Args:
            rectangles (list[tuple[int, int, tuple[int, int, int]]]): 
                A list of tuples, each containing the x and y coordinates and the (r, g, b) color of the rectangle.

        Returns:
            None
        """
        rectangles_for_drawing = []

        for rect in rectangles:
            x, y, color = rect
            r, g, b = color

            if not 0 <= r <= 255 or not 0 <= g <= 255 or not 0 <= b <= 255:
                raise ValueError("Parametrs r, g, b must be in range of (0, 256)")
                
            if not (0 <= x < self.maze_size and 0 <= y < self.maze_size):
                raise ValueError("Parametrs x and y must be in range of the maze size")
            
            rectangles_for_drawing.append((x, y, (r, g, b)))

            row, col = y, x

            if color == self.path_color:
                self.grid[row,col] = 1  
            elif color == self.wall_color:
                self.grid[row,col] = 0 

        self.draw_queue.put(rectangles_for_drawing) 
        
    def erase_rectangle(self, pos: tuple[int, int]) -> None:
        """
        Erases a rectangle at the position (draws wall).
        
        Args:
            pos: The pygame position of the event to erase the rectangle.

        Returns:
            None
        """
        self.draw_rectangle(pos, color=self.wall_color)

    def erase_rectangle_at_square(self, x: int, y: int) -> None:
        """
        Erases a rectangle at the specified square coordinates (draws wall).
        
        Args:
            x (int): X coordinate of the square.
            y (int): Y coordinate of the square.
            
        Returns:
            None
        """
        self.draw_rectangle_at_square(x, y, color=self.wall_color)