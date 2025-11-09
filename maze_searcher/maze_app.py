import queue
import sys
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
        self.screen_size_px = self.maze.maze_size * self.block_size_px

        self.wall_color = maze.wall_color
        self.path_color = maze.path_color

        # Flags for maze generation
        self.space_pressed = False
        self.space_hold_start_time = 0
        self.space_hold_threshold = 1000 
        self.last_auto_step_time = 0
        self.space_held = False
        self.run_next_step = True

        # Flags for drawing on the window
        self.drawing = False
        self.erasing = False

        self.virtual_surface = pygame.Surface((self.screen_size_px, self.screen_size_px))

    def run(self) -> None:
        """
        Starts the Pygame application and runs the main loop.

        Returns:
            None
        """
        self.running = True

        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_size_px, self.screen_size_px), pygame.RESIZABLE)
        
        self.screen.fill(self.wall_color) 
        pygame.display.flip()

        clock = pygame.time.Clock()

        while self.running:
            self._handle_tasks()
            self._handle_events()
            self._handle_drawing()

            # Scale virtual surface onto the real screen (letterboxed square viewport)
            viewport = self.get_square_viewport(self.screen.get_size())
            scaled = pygame.transform.smoothscale(self.virtual_surface, (viewport.width, viewport.height))
            self.screen.fill((0, 0, 0))  # black letterbox
            self.screen.blit(scaled, viewport.topleft)
            
            pygame.display.flip()
            clock.tick(60)

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
                if self.run_next_step:
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

                    if rectangle_list_to_draw:
                        self.maze.draw_rectangle_list(rectangle_list_to_draw)

                    self.run_next_step = False
                    self.last_auto_step_time = pygame.time.get_ticks()

                now = pygame.time.get_ticks()

                if not show_process:
                    self.run_next_step = True

                elif by_space_bar:   
                    # If space bar is held, auto step with delay
                    if self.space_held and now - self.last_auto_step_time >= delay_ms:
                        self.last_auto_step_time = now
                        self.run_next_step = True

                    # Else if space bar was just pressed, advance one step
                    elif self.space_pressed:
                        self.run_next_step = True
                        self.space_pressed = False                  
                else:
                    # If not using space bar, auto step with delay
                    if now - self.last_auto_step_time >= delay_ms:
                        self.last_auto_step_time = now
                        self.run_next_step = True

                self.post_task(step)

            except StopIteration:
                return
            
        self.post_task(step)
            
        
    def get_square_viewport(self, screen_size: tuple[int, int]) -> pygame.Rect:
        sw, sh = screen_size
        size = min(sw, sh)
        x = (sw - size) // 2
        y = (sh - size) // 2
        return pygame.Rect(x, y, size, size)

    def scale_mouse_to_virtual(self, event, screen) -> tuple[int, int] | None:
        """
        Convert a mouse position on the real screen into grid (cell) integer coordinates on the virtual canvas.
        """
        viewport = self.get_square_viewport(screen.get_size())
        pos = event.pos

        if not viewport.collidepoint(pos):
            return None
        
        # pos within viewport
        vx = pos[0] - viewport.x
        vy = pos[1] - viewport.y

        # scale factor from viewport to virtual pixels
        scale = self.screen_size_px / viewport.width
        virtual_x = vx * scale
        virtual_y = vy * scale
        
        return (virtual_x, virtual_y)

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

                pygame.draw.rect(self.virtual_surface, 
                                    color, 
                                    (x * self.block_size_px,
                                    y * self.block_size_px, 
                                    self.block_size_px, 
                                    self.block_size_px))

    def _handle_events(self) -> None:
        """
        Handles Pygame events such as quitting, resizing, mouse actions, and key presses.
        
        Returns:
            None
        """
        events = pygame.event.get()
        self._handle_screen_events(events=events)
        self._handle_key_events(events=events)

    def _handle_screen_events(self, events) -> None:
        """
        Handles events related to the Pygame window, such as quitting and resizing.
        
        Returns:
            None
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                w, h = event.w, event.h
                size = int((w + h) / 2)
                self.screen = pygame.display.set_mode((size, size), pygame.RESIZABLE)

    def _handle_key_events(self, events) -> None:
        """
        Handles Pygame events such as mouse actions, and key presses.
        
        Returns:
            None
        """
        for event in events:   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.drawing = True
                    self.erasing = False
                    pos = self.scale_mouse_to_virtual(event, self.screen)
                    if pos is not None:
                        self.maze.draw_rectangle(pos)
                elif event.button == 3:
                    self.drawing = False
                    self.erasing = True
                    pos = self.scale_mouse_to_virtual(event, self.screen)
                    if pos is not None:
                        self.maze.erase_rectangle(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
                self.erasing = False

            elif event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    pos = self.scale_mouse_to_virtual(event, self.screen)
                    if pos is not None:
                        self.maze.draw_rectangle(pos)
                if self.erasing:
                    pos = self.scale_mouse_to_virtual(event, self.screen)
                    if pos is not None:
                        self.maze.erase_rectangle(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.space_pressed = True
                    self.space_hold_start_time = pygame.time.get_ticks()          

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_pressed = False
                    self.space_held = False
                    self.space_hold_start_time = 0
                    self.last_auto_step_time = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if(now - self.space_hold_start_time >= self.space_hold_threshold):
                self.space_held = True 
