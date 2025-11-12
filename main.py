from maze_searcher import Maze, MazeApp, MazeGeneratorAlgorithm

maze = Maze(35)
app = MazeApp(maze)

# Schedule initial tasks before running
app.post_task(lambda: app.generate(type=MazeGeneratorAlgorithm.KRUSKAL, show_process=False))

# Start the interactive maze window
app.run()