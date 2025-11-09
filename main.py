from maze_searcher import Maze, MazeApp, MazeGeneratorAlgorithm

maze = Maze(35, wall_color=(0,0,0), path_color=(255,255,255))
app = MazeApp(maze)

# Schedule initial tasks before running
app.post_task(lambda: app.generate(type=MazeGeneratorAlgorithm.KRUSKAL, show_process=True, by_space_bar=False, delay_ms=25))

# Start the interactive window (blocking)
app.run()