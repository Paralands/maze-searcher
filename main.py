from maze_searcher import Maze, MazeApp, MazeGeneratorAlgorithm

maze = Maze(35)
app = MazeApp(maze)

# Schedule initial tasks before running
app.post_task(lambda: app.generate(type=MazeGeneratorAlgorithm.DFS, show_process=True, by_space_bar=False, delay_ms=50))

# Start the interactive window (blocking)
app.run()