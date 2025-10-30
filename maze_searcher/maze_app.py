import queue
import numpy as np
import pygame

from maze_searcher.maze_generator_algorithm import MazeGeneratorAlgorithm
from .maze import Maze


class MazeApp:
    """
    MazeApp class responsible for running the maze application with Pygame.
    """

    def __init__(self, maze: Maze):
        """
        Initializes a MazeApp object with the specified maze.
        :param maze: The Maze object to be used in the application.
        """
        self.maze: Maze = maze
        self.task_queue = queue.Queue()
        self.running = False
        self.block_size_px = maze.block_size_px
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        """
        Starts the Pygame application and runs the main loop.

        Returns:
            None
        """
        self.running = True

        pygame.init()

        self.screen = pygame.display.set_mode((self.maze.maze_size*10, self.maze.maze_size*10))
        self.screen.fill((255, 255, 255)) 

        while self.running:
            self._handle_tasks()
            self._handle_events()
            self._handle_drawing()
            pygame.display.flip()
            print("Tick")
            self.clock.tick(60)  # Limit to 60 FPS


        pygame.quit()

    def post_task(self, task) -> None:
        """
        Posts a task to be executed in the main loop.

        Args:
            task: A callable task to be executed.

        Returns:
            None
        """
        self.task_queue.put(task) 

    def generate(self, type: MazeGeneratorAlgorithm = MazeGeneratorAlgorithm.DFS, show_process: bool = False, by_space_bar: bool = False, delay_ms: int = 10) -> None:
        """
        Generates the maze using the specified algorithm and visualizes the process.

        Args:
            type (MazeGeneratorAlgorithm): The maze generation algorithm to use (default is DFS).
            show_process (bool): If True, visualizes the process of generation (default is False).
            by_space_bar (bool): If True, advances the generation step by step using the space bar (default is False).
            delay_ms (int): Delay in milliseconds between steps when not using space bar (default is 10), ignored if by_space_bar is True.

        Returns:
            None
        """
        generator = self.maze.generate(type=type)

        def step():
            try:
                grid = next(generator)

                for (i, j), value in np.ndenumerate(grid):

                    # 0 = wall (white), 1 = path (black)

                    rectangle_list_to_draw = []

                    if value == 1 and self.maze.grid[i, j] == 0:
                        print("Updated path at:", i, j)
                        rectangle_list_to_draw.append((i, j, 0, 0, 0))
                    elif value == 0 and self.maze.grid[i, j] == 1:
                        print("Updated path at:", i, j)
                        rectangle_list_to_draw.append((i, j, 255, 255, 255))

                    if rectangle_list_to_draw != []:
                        self.maze.draw_rectangle_list(rectangle_list_to_draw)

                self.post_task(step)    
                # if by_space_bar:
                    #TODO: implement space bar functionality
                # else:

                #if not by_space_bar:
                #    print("Waiting ...")
                #    pygame.time.wait(delay_ms)
            except StopIteration:
                return

        self.post_task(step)   

    #TODO: redo this method to be more practical
    def post_task_repeated(self, task, delay_ms=10):
        next_time = pygame.time.get_ticks() + delay_ms

        def repeated_task():
            nonlocal next_time

            now = pygame.time.get_ticks()
            if now >= next_time:
                try:
                    task()
                except StopIteration:
                    return
                next_time = now + delay_ms
            self.post_task(repeated_task) 

        self.post_task(repeated_task)

    def _handle_tasks(self):
        """
        Handles and executes tasks from the task queue.
        
        Returns:
            None
        """
        if not self.task_queue.empty():
            print("Handling task...")
            task = self.task_queue.get()
            task()

    def _handle_drawing(self):
        """
        Handles drawing operations from the maze's draw queue.
        
        Returns:
            None
        """
        if not self.maze.draw_queue.empty():
            print("Handling drawing...")
            rectangles = self.maze.draw_queue.get()

            print("Rectangles to draw:", rectangles)

            for rect in rectangles:
                x, y, (r, g, b) = rect
                color = (r, g, b)

                print("Drawing rectangle at:", x, y, "with color:", color)

                if color == (0, 0, 0):
                    print(f"Drawing at ({x}, {y}) with color {color}")
                pygame.draw.rect(self.screen, 
                                    color, 
                                    (x * self.block_size_px,
                                    y * self.block_size_px, 
                                    self.block_size_px, 
                                    self.block_size_px))
                print("Drawing done.")

    def _handle_events(self):
        
        drawing = False
        erasing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    erasing = False
                    self.maze.draw_rectangle(event)
                elif event.button == 3:
                    drawing = False
                    erasing = True
                    self.maze.erase_rectangle(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                erasing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    self.maze.draw_rectangle(event)
                if erasing:
                    self.maze.erase_rectangle(event)