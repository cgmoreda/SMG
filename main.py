import pygame
import heapq
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 21, 21
CELL_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50,100)
Goal = (255, 215, 0)
Player = (0, 255, 0)
Background = BLACK
Walls = WHITE

FONT = pygame.font.Font(None, 36)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Maze Explorer")

# Maze generation using Depth-First Search
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = [(1, 1)]
    visited = set((1, 1))
    # 0 == white && 1 == black
    while stack:
        x, y = stack[-1]
        maze[x][y] = 0
        neighbors = []

        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < rows and 0 < ny < cols and (nx, ny) not in visited:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            stack.append((nx, ny))
            visited.add((nx, ny))
            maze[(x + nx) // 2][(y + ny) // 2] = 0
        else:
            stack.pop()

    return maze

# Heuristic for A* (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Pathfinding Algorithm
def a_star_search(maze, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in neighbors:
            neighbor_pos = (current[0] + neighbor[0], current[1] + neighbor[1])
            if 0 <= neighbor_pos[0] < len(maze) and 0 <= neighbor_pos[1] < len(maze[0]):
                if maze[neighbor_pos[0]][neighbor_pos[1]] == 1:
                    continue

                tentative_g_score = g_score[current] + 1
                if neighbor_pos not in g_score or tentative_g_score < g_score[neighbor_pos]:
                    came_from[neighbor_pos] = current
                    g_score[neighbor_pos] = tentative_g_score
                    f_score[neighbor_pos] = g_score[neighbor_pos] + heuristic(neighbor_pos, goal)
                    heapq.heappush(open_list, (f_score[neighbor_pos], neighbor_pos))

    return None

# Draw the maze
def draw_maze(maze):
    for i in range(ROWS):
        for j in range(COLS):
            color = Walls if maze[i][j] == 0 else Background
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw the path
def draw_path(path):
    for pos in path:
        pygame.draw.rect(screen, BLUE, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Draw button
def draw_button(text, font, color, surface, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))
    text_obj = font.render(text, True, Background)
    text_rect = text_obj.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_obj, text_rect)
    return pygame.Rect(x, y, width, height)

# Main Menu
def main_menu():
    while True:
        screen.fill(Background)
        draw_text('AI Maze Explorer', FONT, Walls, screen, WIDTH // 2, HEIGHT // 4)
        start_button = draw_button('Start', FONT, GREEN, screen, WIDTH // 2 - WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main()
                    return

# Main game function
def main():
    clock = pygame.time.Clock()
    player_pos = [1, 1]
    goal_pos = [ROWS - 2, COLS - 2]
    ai_mode = False
    maze = generate_maze(ROWS, COLS)  # Initial maze generation
    start_time = time.time()  # Start timer

    def regenerate_maze():
        nonlocal maze
        maze = generate_maze(ROWS, COLS)
        # Ensure goal is still reachable
        while not a_star_search(maze, tuple(player_pos), tuple(goal_pos)):
            maze = generate_maze(ROWS, COLS)

    running = True
    while running:
        screen.fill(Background)
        draw_maze(maze)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if a_star_search(maze, tuple(player_pos), tuple(goal_pos)):
                        ai_mode = not ai_mode
                        if ai_mode:
                            ai_path = a_star_search(maze, tuple(player_pos), tuple(goal_pos))

        # Player movement
        keys = pygame.key.get_pressed()
        if not ai_mode:
            if keys[pygame.K_UP] and player_pos[0] > 0 and maze[player_pos[0] - 1][player_pos[1]] == 0:
                player_pos[0] -= 1
            if keys[pygame.K_DOWN] and player_pos[0] < ROWS - 1 and maze[player_pos[0] + 1][player_pos[1]] == 0:
                player_pos[0] += 1
            if keys[pygame.K_LEFT] and player_pos[1] > 0 and maze[player_pos[0]][player_pos[1] - 1] == 0:
                player_pos[1] -= 1
            if keys[pygame.K_RIGHT] and player_pos[1] < COLS - 1 and maze[player_pos[0]][player_pos[1] + 1] == 0:
                player_pos[1] += 1

        # Check if player reached the goal
        if player_pos == goal_pos:
            running = False

        # AI Mode
        if ai_mode:
            if a_star_search(maze, tuple(player_pos), tuple(goal_pos)):
                ai_path = a_star_search(maze, tuple(player_pos), tuple(goal_pos))
                if ai_path:
                    ai_path.pop(0)
                    if ai_path:
                        next_pos = ai_path.pop(0)
                        player_pos = list(next_pos)
                else:
                    ai_mode = False

        pygame.draw.rect(screen, Player, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, Goal, (goal_pos[1] * CELL_SIZE, goal_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Display the timer
        elapsed_time = time.time() - start_time
        draw_text(f'Time: {elapsed_time:.2f} sec', FONT, Walls, screen, WIDTH // 2, 10)

        pygame.display.flip()
        clock.tick(10)  # Adjust the speed of the AI here

    # End game screen
    end_time = time.time()
    total_time = end_time - start_time
    screen.fill(Background)
    draw_text('Congratulations!', FONT, GREEN, screen, WIDTH // 2, HEIGHT // 3)
    draw_text(f'Your time: {total_time:.2f} seconds', FONT, Walls, screen, WIDTH // 2, HEIGHT // 2)
    draw_text('Press any key to return to main menu', FONT, Walls, screen, WIDTH // 2, 2 * HEIGHT // 3)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                main_menu()

if __name__ == "__main__":
    main_menu()
