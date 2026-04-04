*This project has been created as part of the 42 curriculum by ael-mora, oel-mora.*

# A-Maze-ing

## Description

A-Maze-ing is a Python project that generates, solves, and displays mazes in the terminal.

The goal of this project is to:

* Generate a valid maze using an algorithm.
* Ensure connectivity between entry and exit.
* Display the maze visually in the terminal.
* Compute the shortest path between entry and exit.
* Export the maze in a specific hexadecimal format.

The maze includes a visible **"42" pattern** made of blocked cells placed in the center of the maze.

---

## Instructions

### Run the program

```bash
python3 a_maze_ing.py config.txt
```

### Project structure

```
a_maze_ing.py        # main entry point
config_parser.py     # parse config file
maze.py              # maze structure
generator.py         # DFS generation
solver.py            # BFS shortest path
pattern.py           # 42 pattern
display.py           # terminal display
writer.py            # export to file
config.txt           # configuration file
```

---

## Configuration File

The program requires a config file with the following format:

```
WIDTH=21
HEIGHT=21
ENTRY=0,0
EXIT=20,20
OUTPUT_FILE=maze_output.txt
PERFECT=True
SEED=42
```

### Fields

* `WIDTH`, `HEIGHT` → maze size
* `ENTRY` → starting point (x,y)
* `EXIT` → ending point (x,y)
* `OUTPUT_FILE` → file where the maze is saved
* `PERFECT`:

  * `True` → only one path (perfect maze)
  * `False` → multiple paths allowed
* `SEED` → optional randomness control

---

## Maze Generation Algorithm

We use the **DFS (Depth-First Search)** algorithm to generate the maze.

### Steps:

1. Start from the entry cell
2. Randomly visit unvisited neighbors
3. Remove walls between cells
4. Backtrack when no neighbors are available

---

## Why DFS?

We chose DFS because:

* It is simple and efficient
* It guarantees a fully connected maze
* It naturally produces a **perfect maze (unique path)**
* Easy to extend for animation

When `PERFECT=False`, we add extra openings to create loops.

---

## Maze Solving Algorithm

We use **BFS (Breadth-First Search)** to find the shortest path.

Why BFS?

* Always finds the shortest path
* Simple to implement
* Works perfectly with grid-based structures

---

## Reusable Module

The `MazeGenerator` class is designed to be reusable:

* Independent from display
* Works with any Maze instance
* Supports:

  * deterministic generation (via seed)
  * animation (via callback)
  * perfect / non-perfect modes

Example usage:

```python
maze = Maze(20, 20, (0,0), (19,19))
generator = MazeGenerator(maze)
generator.generate()
```

---

## Features

* Maze generation (DFS)
* Shortest path (BFS)
* Terminal display with colors
* Show / hide path
* Regenerate maze
* Multiple color themes
* 42 pattern inside the maze
* Export to file

---

## Team & Project Management

### 👤 Team

* ael-mora → display, interaction & output, pattern 42
* oel-mora → Maze generation (DFS), Solver (BFS),  core logic

---

### Planning

Initial plan:

* Build maze structure
* Implement DFS generation
* Add BFS solver
* Add display system
* Add config parsing

Evolution:

* Added 42 pattern in the center
* Added PERFECT=False mode
* Improved validation and error handling
* Refactored code into modules

---

### What worked well

* Clear separation of responsibilities
* DFS + BFS integration was stable
* Modular design made debugging easier

---

### What could be improved

* Better centering of 42 pattern
* Optimization for large mazes
* Add more generation algorithms (Prim, Kruskal)

---

### Tools Used

* Python 3.10+
* Terminal (ANSI colors)
* Git

---

## AI Usage

AI was used for:

* Understanding DFS and BFS algorithms
* Structuring the project into modules
* Debugging errors and edge cases
* Improving code readability and organization
* Generating README structure

All generated content was reviewed and adapted manually.

---

## Resources

* DFS Algorithm
  https://en.wikipedia.org/wiki/Depth-first_search

* BFS Algorithm
  https://en.wikipedia.org/wiki/Breadth-first_search

* Maze generation (recursive backtracking)
  https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking

* ANSI colors
  https://en.wikipedia.org/wiki/ANSI_escape_code
