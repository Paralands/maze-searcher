import queue
import numpy as np
import pygame

from .algorithms import MazeGeneratorAlgorithm
from .maze import Maze


class MazeApp:
    """
    MazeApp class responsible for running the maze application with Pygame.
    """

    def __init__(self, maze: Maze):
        """
        Initializes a MazeApp object with the specified maze.
        
        Args:
            maze (Maze): The maze to be visualized and interacted with.
        """
        self.maze: Maze = maze
        self.block_size_px = maze.block_size_px
        self.task_queue = queue.Queue()

        self.running = False
        self.screen_size_px = self.maze.maze_size * self.maze.block_size_px

        self.wall_color = maze.wall_color
        self.path_color = maze.path_color

        # Flags for maze generation
        self.wait_for_space_bar = True
        self.space_held = False
        self.space_hold_start_time = 0
        self.space_hold_threshold = 1000 # in ms

        # Flags for drawing on the window
        self.drawing = False
        self.erasing = False

    def run(self) -> None:
        """
        Starts the Pygame application and runs the main loop.

        Returns:
            None
        """
        self.running = True

        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.screen_size_px, 
             self.screen_size_px))
        
        self.screen.fill(self.wall_color) 
        pygame.display.flip()

        while self.running:
            self._handle_tasks()
            self._handle_events()
            self._handle_drawing()
            
            pygame.display.flip()

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

    def generate(self, type: MazeGeneratorAlgorithm = MazeGeneratorAlgorithm.DFS, show_process: bool = False, by_space_bar: bool = False, delay_ms: int = 50) -> None:
        """
        Generates the maze using the specified algorithm and visualizes the process. 

        Args:
            type (MazeGeneratorAlgorithm): The maze generation algorithm to use (default is DFS).
            show_process (bool): If True, visualizes the process of generation (default is False).
            by_space_bar (bool): If True, advances the generation step by step using the space bar, and makes it automatic with the delay if the space bar is held (default is False)
            delay_ms (int): Delay in milliseconds between steps when not using space bar (default is 10), used to delay faster generation if by_space_bar is True.

        Returns:
            None
        """
        generator = self.maze.generate(type=type)

        def step():
            try:
                grid = next(generator)

                rectangle_list_to_draw = []

                # Check for the grid updates
                for (row, col), value in np.ndenumerate(grid):
                    x, y = col, row
                    
                    # 0 = wall, 1 = path
                    if value == 1 and self.maze.grid[row, col] == 0:
                        rectangle_list_to_draw.append((x, y, self.path_color))
                    elif value == 0 and self.maze.grid[row, col] == 1:
                        rectangle_list_to_draw.append((x, y, self.wall_color))

                if rectangle_list_to_draw != []:
                    self.maze.draw_rectangle_list(rectangle_list_to_draw)

                if show_process:     
                    if by_space_bar:   
                        while self.wait_for_space_bar:
                            if self.space_held:
                                pygame.time.wait(delay_ms)
                                break
                            
                            # Check if space was pressed
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        self.space_hold_start_time = pygame.time.get_ticks()
                                        self.wait_for_space_bar = False
                            
                            # Check if space is being held
                            keys = pygame.key.get_pressed()
                            if keys[pygame.K_SPACE]:
                                if not self.space_held:
                                    held_time = pygame.time.get_ticks() - self.space_hold_start_time
                                    if held_time >= self.space_hold_threshold:
                                        self.space_held = True

                        self.wait_for_space_bar = True
                    else:
                        pygame.time.wait(delay_ms)
                
                self._handle_exits()
                self.post_task(step)

            except StopIteration:
                return

        self.post_task(step)   

    def _handle_tasks(self) -> None:
        """
        Handles and executes tasks from the task queue.
        
        Returns:
            None
        """
        if not self.task_queue.empty():
            task = self.task_queue.get()
            task()

    def _handle_drawing(self) -> None:
        """
        Handles drawing operations from the maze's draw queue.
        
        Returns:
            None
        """
        if not self.maze.draw_queue.empty():
            rectangles = self.maze.draw_queue.get()

            for rect in rectangles:
                x, y, (r, g, b) = rect
                color = (r, g, b)

                pygame.draw.rect(self.screen, 
                                    color, 
                                    (x * self.block_size_px,
                                    y * self.block_size_px, 
                                    self.block_size_px, 
                                    self.block_size_px))

    def _handle_exits(self) -> None:
        """
        Handles exiting the application.
        
        Returns:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _handle_events(self) -> None:
        """
        Handles Pygame events such as quitting, mouse actions, and key presses.
        
        Returns:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.drawing = True
                    self.erasing = False
                    self.maze.draw_rectangle(event)
                elif event.button == 3:
                    self.drawing = False
                    self.erasing = True
                    self.maze.erase_rectangle(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
                self.erasing = False

            elif event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    self.maze.draw_rectangle(event)
                if self.erasing:
                    self.maze.erase_rectangle(event)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_hold_start_time = 0
                    self.space_held = False

        