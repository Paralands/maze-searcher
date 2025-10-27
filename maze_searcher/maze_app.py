import queue
import pygame
from .maze import Maze


class MazeApp:
    def __init__(self, maze: Maze):
        self.maze: Maze = maze
        self.task_queue = queue.Queue()
        self.running = False
        self.block_size_px = maze.block_size_px
        self.clock = pygame.time.Clock()

    def run(self):
        self.running = True

        pygame.init()

        self.screen = pygame.display.set_mode((self.maze.maze_size*10, self.maze.maze_size*10))
        self.screen.fill((0, 0, 0)) 

        while self.running:
            self._handle_tasks()
            self._handle_events()
            self._handle_drawing()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def post_task(self, task):
        self.task_queue.put(task)    

    #TODO: redo this method to be more practical
    def post_task_repeated(self, task, delay_ms=10, by_space_bar=False):
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
        while not self.task_queue.empty():
            task = self.task_queue.get()
            task()

    def _handle_drawing(self):
        while not self.maze.draw_queue.empty():
            x, y, color = self.maze.draw_queue.get()
            pygame.draw.rect(self.screen, 
                                color, 
                                (x * self.block_size_px,
                                y * self.block_size_px, 
                                self.block_size_px, 
                                self.block_size_px))

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