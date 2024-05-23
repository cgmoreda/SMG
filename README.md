# SMG (Simple Maze Game)

## Overview

Simple Maze Game is a Python-based game that generates a maze using the Depth-First Search algorithm and allows the player to navigate through it manually or by using an AI-powered A* pathfinding algorithm. The player starts at the top-left corner of the maze and must reach the goal at the bottom-right corner.

## Features

- **Maze Generation:** The maze is generated using the Depth-First Search algorithm, ensuring a unique maze every time.
- **Manual Control:** The player can navigate the maze using the arrow keys.
- **AI Pathfinding:** The AI can take over using the A* pathfinding algorithm to find the shortest path to the goal.
- **Timing:** The game tracks the time taken to reach the goal.

## Installation

1. Ensure you have Python installed (preferably Python 3.7 or later).
2. Install the required libraries using pip:
   ```bash
   pip install pygame
   ```

## How to Run

1. Save the provided code into a file named `maze_explorer.py`.
2. Run the script:
   ```bash
   python maze_explorer.py
   ```

## Controls

- **Arrow Keys:** Move the player up, down, left, or right.
- **A Key:** Toggle AI mode. The AI will automatically find the path to the goal if this mode is enabled.

## Code Structure

- **Constants:** Define colors, dimensions, and other constants used in the game.
- **Pygame Initialization:** Initialize Pygame and create the game window.
- **Maze Generation:** Function to generate the maze using Depth-First Search.
- **Heuristic Function:** Calculate the Manhattan distance used in the A* algorithm.
- **A* Pathfinding Algorithm:** Find the shortest path from the start to the goal.
- **Drawing Functions:** Functions to draw the maze, path, text, and buttons.
- **Main Menu:** Display the main menu and start the game.
- **Main Game Function:** Handle game logic, including player movement, AI control, and timing.

## Functions

### `generate_maze(rows, cols)`
Generates a maze using Depth-First Search.

### `heuristic(a, b)`
Calculates the Manhattan distance between two points.

### `a_star_search(maze, start, goal)`
Implements the A* pathfinding algorithm to find the shortest path in the maze.

### `draw_maze(maze)`
Draws the maze on the screen.

### `draw_path(path)`
Draws the path found by the A* algorithm.

### `draw_text(text, font, color, surface, x, y)`
Displays text on the screen.

### `draw_button(text, font, color, surface, x, y, width, height)`
Draws a button and returns its rectangle.

### `main_menu()`
Displays the main menu and waits for the player to start the game.

### `main()`
Main game loop handling game logic, player movement, AI control, and timing.

## How to Play

1. Start the game and click "Start" on the main menu.
2. Navigate the maze using the arrow keys.
3. Press the "A" key to toggle AI mode and let the AI find the path to the goal.
4. Reach the goal at the bottom-right corner as quickly as possible.
5. View your time and return to the main menu to play again.

## End Screen

Upon reaching the goal, the total time taken is displayed. Press any key to return to the main menu and start a new game.

Enjoy exploring the maze with the Simple Maze Game!
