import queue
import numpy as np
import pygame

from .algorithms import MazeGeneratorAlgorithm
from .algorithms.maze_solver_algorithm import MazeSolverAlgorithm
from .maze import Maze

class MazeApp:
    """
    MazeApp class responsible for running the maze application with Pygame.

    Public Methods:
        - __init__(maze: Maze, default_delay_ms: int = 25) -> None
        - run() -> None
        - post_task(task) -> None
        - generate(type: MazeGeneratorAlgorithm = MazeGeneratorAlgorithm.DFS, delay_ms: int = 25, show_process: bool = True) -> None
        - solve() -> None
        - reset() -> None
        - stop_animation() -> None
    """

    def __init__(self, maze: Maze, default_delay_ms: int = 25) -> None:
        """
        Initializes a MazeApp object with the specified maze.
        
        Args:
            maze (Maze): The maze to be visualized and interacted with.
            default_delay_ms (int): Default delay in milliseconds for generation/solving steps (default is 50).
        """
        self.maze: Maze = maze

        self.task_queue = queue.Queue()

        self.running = False

        # Screen and drawing parameters, will be set in run()
        self.screen_size_px = self.maze.block_size_px * self.maze.maze_size
        self.block_size_px = self.maze.block_size_px

        # Colors
        self.wall_color = maze.wall_color
        self.path_color = maze.path_color
        self.visited_color = maze.visited_color
        self.start_color = maze.start_color
        self.goal_color = maze.goal_color
        self.solution_color = maze.solution_color

        # Flags for maze solving and generation
        self.solving = False
        self.generating = False
        self.run_next_step = True

        # Flags and parameters for step delays
        self.delay_ms = default_delay_ms
        self.wait_for_space = False
        self.space_pressed = False
        self.space_held = False
        self.control_pressed = False
        self.space_hold_start_time = 0
        self.space_hold_threshold = 1000 
        self.last_auto_step_time = 0
        self.last_ctrl_combo_time = 0
        self.ctrl_combo_cooldown = 200  

        # Flags for drawing on the window
        self.drawing = False
        self.erasing = False

        # Flags for key presses
        self.pressed_s = False
        self.pressed_g = False

        self.virtual_surface = pygame.Surface((self.screen_size_px, self.screen_size_px))
    
    def run(self) -> None:
        """
        Starts the Pygame application and runs the main loop.

        Returns:
            None
        """
        self.running = True

        pygame.init()

        self._set_block_size_px()
        self.screen = pygame.display.set_mode((self.screen_size_px, self.screen_size_px), pygame.RESIZABLE)
        
        self.screen.fill(self.wall_color) 
        pygame.display.flip()

        clock = pygame.time.Clock()

        while self.running:
            self._handle_tasks()
            self._handle_events()
            self._handle_drawing()

            # Scale virtual surface onto the real screen (letterboxed square viewport)
            viewport = self._get_square_viewport(self.screen.get_size())
            scaled = pygame.transform.scale(self.virtual_surface, (viewport.width, viewport.height))
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
        if not callable(task):
            raise ValueError("Task must be a callable function or method.")

        self.task_queue.put(task) 

    def generate(self, type: MazeGeneratorAlgorithm = MazeGeneratorAlgorithm.DFS, delay_ms: int = 25, show_process: bool = True) -> None:
        """
        Generates the maze using the specified algorithm and visualizes the process. 

        Args:
            type (MazeGeneratorAlgorithm): The maze generation algorithm to use (default is DFS).
            delay_ms (int): Delay in milliseconds between steps (default is 25).
            show_process (bool): Whether to visualize the generation process (default is True).

        Returns:
            None
        """
        self.reset()
        generator = self.maze.generate(type=type)
        self.generating = True

        if generator is None:
            return

        def step():
            try:
                if not self.generating:
                    return

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

                if show_process:
                    self._check_for_delay(delay_ms)
                else:
                    self.run_next_step = True

                self.post_task(step)

            except StopIteration:
                return
            
        self.post_task(step)
    
    def solve(self, type: MazeSolverAlgorithm = MazeSolverAlgorithm.ASTAR) -> None:
        """
        Solves the maze using the maze's solve method and visualizes the process.

        Args:
            type (MazeSolverAlgorithm): The maze solving algorithm to use (default is A*).

        Returns:
            None
        """
        self.stop_animation()
        self.maze.clear_solving()
        
        solver = self.maze.solve(type=type)
        self.solving = True

        if solver is None:
            return

        def step():
            try:
                if not self.solving:
                    return

                if self.run_next_step:
                    grid = next(solver)

                    rectangle_list_to_draw = []

                    # Check for the grid updates
                    for (row, col), value in np.ndenumerate(grid):
                        x, y = col, row
                        
                        # 0 = wall, 1 = path, 2 = visited, 3 = start, 4 = goal, 5 = solution
                        if value == 2 and self.maze.grid[row, col] != 2:
                            rectangle_list_to_draw.append((x, y, self.visited_color))

                        if value == 5 and self.maze.grid[row, col] != 5:
                            rectangle_list_to_draw.append((x, y, self.solution_color))

                    if rectangle_list_to_draw:
                        self.maze.draw_rectangle_list(rectangle_list_to_draw)

                    self.run_next_step = False
                    self.last_auto_step_time = pygame.time.get_ticks()

                self._check_for_delay(self.delay_ms)
                self.post_task(step)

            except StopIteration:
                return
            
        self.post_task(step)

    def reset(self) -> None:
        """
        Resets the maze to its initial state.

        Returns:
            None
        """
        self.stop_animation()
        self.maze.reset()

    def stop_animation(self) -> None:
        """
        Stops any ongoing maze generation or solving animation.

        Returns:
            None
        """
        self.solving = False
        self.generating = False
        self.wait_for_space = False
        self._clear_task_queue()
    
    def _clear_task_queue(self) -> None:
        """
        Clears all pending tasks from the task queue.

        Returns:
            None
        """
        while not self.task_queue.empty():
            try:
                self.task_queue.get_nowait()
            except queue.Empty:
                break

    def _check_for_delay(self, delay_ms) -> None:
        """
        Checks if the specified delay has passed and updates the run_next_step flag accordingly.
        Args:
            delay_ms (int): The delay in milliseconds.
        Returns:
            None
        """
        now = pygame.time.get_ticks()

        if self.wait_for_space:   
            # If space bar is held, auto step with delay
            if self.space_held and now - self.last_auto_step_time >= delay_ms:
                self.last_auto_step_time = now
                self.run_next_step = True

            # Else if space bar was just pressed, advance one step
            elif self.space_pressed:
                self.run_next_step = True
                self.space_pressed = False
        elif self.space_pressed:
            self.run_next_step = True
            self.space_pressed = False
            self.wait_for_space = True                  
        else:
            # Default to auto step with delay
            if now - self.last_auto_step_time >= delay_ms:
                self.last_auto_step_time = now
                self.run_next_step = True

    def _set_block_size_px(self) -> None:
        """
        Sets the block size in pixels to fit the maze within 85% of the screen's smaller dimension.
        Must be called after pygame.init() before using the MazeApp.

        Returns:
            None
        """
        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h
        self.maze.set_block_size_px((min(screen_width * 0.85, screen_height * 0.85) // self.maze.maze_size) )
        
        # Setting essential parameters
        self.block_size_px = self.maze.block_size_px
        self.screen_size_px = self.maze.maze_size * self.block_size_px
        self.virtual_surface = pygame.Surface((self.screen_size_px, self.screen_size_px))

    def _get_square_viewport(self, screen_size: tuple[int, int]) -> pygame.Rect:
        sw, sh = screen_size
        size = min(sw, sh)
        x = (sw - size) // 2
        y = (sh - size) // 2
        return pygame.Rect(x, y, size, size)

    def _scale_mouse_to_virtual(self, event, screen) -> tuple[int, int] | None:
        """
        Convert a mouse position on the real screen into grid (cell) integer coordinates on the virtual canvas.
        """
        viewport = self._get_square_viewport(screen.get_size())
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
    
    def _get_current_color(self):
        """
        Returns the color based on the current drawing mode.
        
        Returns:
            tuple[int, int, int]: The RGB color for drawing.
        """
        if self.drawing:
            if self.pressed_s:
                return self.maze.start_color
            elif self.pressed_g:
                return self.maze.goal_color
            return self.maze.wall_color
        elif self.erasing:
            return self.maze.path_color
        return None

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
        pressed_keys = set()

        for event in events:   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.drawing = True
                    self.erasing = False
                elif event.button == 3:
                    self.drawing = False
                    self.erasing = True

                pos = self._scale_mouse_to_virtual(event, self.screen)
                if pos is not None:
                    color = self._get_current_color()
                    if color is not None:
                        self.maze.draw_rectangle(pos, color=color)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
                self.erasing = False

            elif event.type == pygame.MOUSEMOTION:
                pos = self._scale_mouse_to_virtual(event, self.screen)
                if pos is not None:
                    color = self._get_current_color()
                    if color is not None:
                        self.maze.draw_rectangle(pos, color=color)

            elif event.type == pygame.KEYDOWN:
                pressed_keys.add(event.key)

                if event.key == pygame.K_SPACE:
                    self.space_pressed = True
                    self.space_hold_start_time = pygame.time.get_ticks() 

                # 'S' key for setting start point
                if event.key == pygame.K_s:
                    self.pressed_s = True

                # 'G' key for setting goal point
                if event.key == pygame.K_g:
                    self.pressed_g = True    

                # 'Y' key for solving the maze using A*
                if event.key == pygame.K_y:
                    self.solve()     

                # 'R' key for resetting the maze
                if event.key == pygame.K_r:
                    self.reset()
                    

                # Ctrl + D/K/P for generating maze with different algorithms
                now = pygame.time.get_ticks()
                if self.control_pressed and (now - self.last_ctrl_combo_time > self.ctrl_combo_cooldown):
                    if event.key == pygame.K_d:
                        self.reset()
                        self.generate(type=MazeGeneratorAlgorithm.DFS, show_process=True)
                        self.last_ctrl_combo_time = now

                    elif event.key == pygame.K_k:
                        self.reset()
                        self.generate(type=MazeGeneratorAlgorithm.KRUSKAL, show_process=True)
                        self.last_ctrl_combo_time = now

                    elif event.key == pygame.K_p:
                        self.reset()
                        self.generate(type=MazeGeneratorAlgorithm.PRIM, show_process=True)
                        self.last_ctrl_combo_time = now

                    elif event.key == pygame.K_s:
                        self.stop_animation()
                        self.last_ctrl_combo_time = now

            elif event.type == pygame.KEYUP:
                pressed_keys.discard(event.key)

                if event.key == pygame.K_SPACE:
                    self.space_pressed = False
                    self.space_held = False
                    self.space_hold_start_time = 0
                    self.last_auto_step_time = 0
                
                if event.key == pygame.K_s:
                    self.pressed_s = False
                
                if event.key == pygame.K_g:
                    self.pressed_g = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if(now - self.space_hold_start_time >= self.space_hold_threshold):
                self.space_held = True 
        else:
            self.space_held = False
        
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            self.control_pressed = True
        else:
            self.control_pressed = False
    
