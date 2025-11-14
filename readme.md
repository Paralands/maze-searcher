# MazeSearcher

**MazeSearcher** is a simple Python application that lets you generate,
edit and solve mazes in an interactive Pygame window.\
Draw walls, place start/goal, watch maze generators run (DFS / Prim /
Kruskal) and see the **A**\* solver animate the pathfinding.

------------------------------------------------------------------------

## What it does

-   Interactive grid editor (draw / erase cells).\
-   Place start and goal cells.\
-   Visual maze generation (DFS, Prim, Kruskal).\
-   Animated A\* solver (step-by-step or automatic).\
-   Resizable window with a scaled viewport.

------------------------------------------------------------------------

## Requirements

-   Python **3.10+**\
-   `pygame`\
-   `numpy`
-   `pandas`

You can install the Python packages with:

``` bash
pip install pygame numpy pandas
# or
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Installation

1.  Clone the repo (or copy files into a folder).\
2.  Create a virtual environment (recommended):

``` bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt 
```

3.  Run:

``` bash
python main.py
```

------------------------------------------------------------------------

## Usage / Controls

| Action                   | Key / Mouse           |
|--------------------------|------------------------|
| Draw walls               | Left-click + drag      |
| Erase walls              | Right-click + drag     |
| Set Start cell           | Hold **S** while drawing |
| Set Goal cell            | Hold **G** while drawing |
| Step once                | **Space** (tap)        |
| Auto-step                | Hold **Space**         |
| Solve with A*            | **Y**                  |
| Reset maze               | **R**                  |
| Generate maze (DFS)      | **Ctrl + D**           |
| Generate maze (Kruskal)  | **Ctrl + K**           |
| Generate maze (Prim)     | **Ctrl + P**           |
| Stop animation           | **Ctrl + S**           |
| Quit                     | Window close button    |

------------------------------------------------------------------------

## License

MIT License. See LICENSE file.
